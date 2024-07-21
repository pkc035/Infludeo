from rest_framework             import generics, status
from rest_framework.response    import Response
from django.db                  import transaction
from django.utils               import timezone
from .models                    import Sale
from .serializers               import SaleListSerializer, SaleDetailSerializer, SaleCreateSerializer


class SaleListView(generics.ListAPIView):
    serializer_class = SaleListSerializer

    def get_queryset(self):
        sales = Sale.objects.filter(state='판매중')
        unique_sales = {}

        for sale in sales:
            if sale.photo_card_id not in unique_sales:
                unique_sales[sale.photo_card_id] = sale
            else:
                current_sale = unique_sales[sale.photo_card_id]
                
                if (sale.price < current_sale.price or
                    (sale.price == current_sale.price and sale.renewal_date < current_sale.renewal_date)):
                    unique_sales[sale.photo_card_id] = sale

        return list(unique_sales.values())


class SaleDetailView(generics.ListAPIView):
    serializer_class = SaleDetailSerializer

    def get_queryset(self):
        photo_card_id = self.kwargs['photo_card_id']
    
        return Sale.objects.filter(photo_card_id=photo_card_id, state='판매완료').order_by('-create_date')[:5]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': '상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleCreateSerializer

class PurchaseView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        sale_id = self.kwargs.get('sale_id')
        try:
            sale = Sale.objects.get(id=sale_id, state='판매중')

        except Sale.DoesNotExist:
            return Response({"detail": "판매중인 항목을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        buyer = request.user

        if buyer.cash < (sale.price + sale.fee):
            return Response({"detail": "잔액이 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if sale.seller == buyer:
            return Response({"detail": "자신이 판매한 항목은 구매할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                sale.state = '판매완료'
                sale.buyer = buyer
                sale.sold_date = timezone.now()
                sale.save()

                buyer.cash -= (sale.price + sale.fee)
                sale.seller.cash += sale.price
                buyer.save()
                sale.seller.save()

        except Exception as e:
            return Response({"detail": "거래 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "구매가 완료되었습니다."}, status=status.HTTP_200_OK)