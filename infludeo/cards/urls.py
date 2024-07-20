from django.urls            import path, include
from rest_framework.routers import DefaultRouter
from .views                 import PhotoCardViewSet

router = DefaultRouter()
router.register(r'', PhotoCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
