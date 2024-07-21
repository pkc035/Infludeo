from django.contrib.auth            import get_user_model
from rest_framework                 import generics
from rest_framework.permissions     import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers                   import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    """
    User 생성 API

    POST 요청을 통해 새로운 User를 생성.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    JWT 토큰 발급 API

    POST 요청을 통해 User의 JWT 액세스 토큰과 리프레시 토큰을 발급.
    """
    serializer_class = CustomTokenObtainPairSerializer
