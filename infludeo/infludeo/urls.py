from django.urls        import path, include
from django.contrib     import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/cards/', include('cards.urls')),
    path('api/sales/', include('sales.urls')),
]