from rest_framework             import generics, status
from rest_framework.response    import Response
from django.db                  import transaction
from django.utils               import timezone
from .models                    import Sale
from .serializers               import SaleListSerializer, SaleDetailSerializer, SaleCreateSerializer


class SaleListView(generics.ListAPIView):
    """
    판매 목록을 조회하는 API

    현재 판매중인 판매 항목만을 목록으로 반환.
    중복된 PhotoCard가 있는 경우, 가격이 가장 낮은 판매 항목만을 반환하며,
    가격이 동일할 경우 수정 날짜가 가장 이른 항목을 반환.
    """
    serializer_class = SaleListSerializer

    def get_queryset(self):
        """
        현재 판매중인 판매 항목의 쿼리셋을 반환.

        중복된 포토카드 ID가 있는 경우, 가격이 가장 낮은 판매 항목만을 선택하며,
        가격이 동일할 경우 수정 날짜가 가장 이른 항목을 선택.

        Returns:
            list: 필터링된 Sale 모델 인스턴스의 list
        """
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
    """
    판매 항목의 세부 정보를 조회하는 API

    특정 PhotoCard에 대한 판매 항목의 세부 사항을 조회할 수 있습니다.
    최근 거래가를 5개까지 조회할 수 있습니다.
    """
    serializer_class = SaleDetailSerializer

    def get_queryset(self):
        """
        특정 PhotoCard와 상태가 '판매완료'인 판매 항목의 쿼리셋을 반환.

        Args:
            None

        Returns:
            QuerySet: 판매 항목 쿼리셋 (최신 거래가를 기준으로 정렬된 상위 5개 항목)
        """
        photo_card_id = self.kwargs['photo_card_id']
    
        return Sale.objects.filter(photo_card_id=photo_card_id, state='판매완료').order_by('-create_date')[:5]

    def get(self, request, *args, **kwargs):
        """
        GET 요청에 대한 처리를 수행.

        Args:
            request (Request): HTTP 요청 객체

        Returns:
            Response: 판매 항목 데이터
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': '상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SaleCreateView(generics.CreateAPIView):
    """
    새로운 판매 항목을 생성하는 API

    PhotoCard의 판매 항목을 생성, 판매자는 요청한 사용자로 설정 됨.
    """
    queryset = Sale.objects.all()
    serializer_class = SaleCreateSerializer

class PurchaseView(generics.GenericAPIView):
    """
    판매 항목을 구매하는 API

    특정 판매 항목을 구매하는 기능을 제공합니다. 구매자는 요청을 보낸 사용자이며,
    판매 항목이 '판매중' 상태일 때만 구매할 수 있습니다. 구매자는 충분한 잔액이 있어야 하며,
    자신이 판매한 항목은 구매할 수 없습니다. 거래 완료 후, 해당 항목의 상태를 '판매완료'로 변경합니다.
    """

    def post(self, request, *args, **kwargs):
        """
        판매 항목을 구매

        Args:
            request (Request): HTTP 요청 객체. 요청 객체에는 구매할 판매 항목의 ID가 포함되어 있어야 합니다.

        Returns:
            Response: 거래 결과에 대한 메시지를 포함하는 HTTP 응답
                - 성공: {"detail": "구매가 완료되었습니다."}
                - 실패:
                  - 판매 항목을 찾을 수 없을 때: {"detail": "판매중인 항목을 찾을 수 없습니다."}
                  - 잔액 부족 시: {"detail": "잔액이 부족합니다."}
                  - 자신이 판매한 항목을 구매하려 할 때: {"detail": "자신이 판매한 항목은 구매할 수 없습니다."}
                  - 거래 처리 중 오류 발생 시: {"detail": "거래 처리 중 오류가 발생했습니다."}
        """
        sale_id = self.kwargs.get('sale_id')
        try:
            # 판매 중인 항목을 조회합니다.
            sale = Sale.objects.get(id=sale_id, state='판매중')

        except Sale.DoesNotExist:
            return Response({"detail": "판매중인 항목을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        buyer = request.user

        # 구매자의 잔액을 확인합니다.
        if buyer.cash < (sale.price + sale.fee):
            return Response({"detail": "잔액이 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 구매자가 판매자와 동일한지 확인합니다.
        if sale.seller == buyer:
            return Response({"detail": "자신이 판매한 항목은 구매할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 데이터베이스 트랜잭션을 사용하여 일관성 있게 처리합니다.
            with transaction.atomic():
                sale.state = '판매완료'
                sale.buyer = buyer
                sale.sold_date = timezone.now()
                sale.save()

                # 구매자와 판매자의 잔액을 업데이트합니다.
                buyer.cash -= (sale.price + sale.fee)
                sale.seller.cash += sale.price
                buyer.save()
                sale.seller.save()

        except Exception as e:
            return Response({"detail": "거래 처리 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "구매가 완료되었습니다."}, status=status.HTTP_200_OK)