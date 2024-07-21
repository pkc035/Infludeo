from rest_framework             import viewsets
from rest_framework.permissions import IsAuthenticated
from .models                    import PhotoCard
from .serializers               import PhotoCardSerializer

class PhotoCardViewSet(viewsets.ModelViewSet):
    """
    PhotoCard 모델에 대한 CRUD API

    PhotoCard 모델의 모든 인스턴스에 대한 조회, 생성, 업데이트, 삭제 작업.
    인증된 사용자만 접근 가능.
    """
    queryset = PhotoCard.objects.all()
    serializer_class = PhotoCardSerializer
