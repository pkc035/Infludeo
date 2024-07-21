from rest_framework             import generics, status
from rest_framework.response    import Response
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
            return Response({'detail': 'No sales found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleCreateSerializer
