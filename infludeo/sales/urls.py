from django.urls import path
from .views import SaleListView, SaleDetailView, SaleCreateView

urlpatterns = [
    path('', SaleListView.as_view(), name='sale-list'),
    path('<int:photo_card_id>/', SaleDetailView.as_view(), name='sale-detail'),
    path('create/', SaleCreateView.as_view(), name='sale-create'),
]
