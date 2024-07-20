from django.contrib.auth            import get_user_model
from rest_framework                 import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers                   import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
