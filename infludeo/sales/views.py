from rest_framework import generics
from .models import Sale
from .serializers import SaleListSerializer, SaleDetailSerializer, SaleCreateSerializer

class SaleListView(generics.ListAPIView):
    serializer_class = SaleListSerializer

    def get_queryset(self):
        sales = Sale.objects.filter(state='판매중')
        unique_sales = {}
        
        for sale in sales:
            if sale.photo_card_id not in unique_sales or (sale.price < unique_sales[sale.photo_card_id].price):
                unique_sales[sale.photo_card_id] = sale
        
        return list(unique_sales.values())

class SaleDetailView(generics.RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleDetailSerializer

    def get_object(self):
        photo_card_id = self.kwargs['photo_card_id']
        return Sale.objects.filter(photo_card_id=photo_card_id).order_by('-create_date')[:5]

class SaleCreateView(generics.CreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleCreateSerializer
