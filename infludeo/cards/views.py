from rest_framework             import viewsets
from rest_framework.permissions import IsAuthenticated
from .models                    import PhotoCard
from .serializers               import PhotoCardSerializer

class PhotoCardViewSet(viewsets.ModelViewSet):
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardSerializer
