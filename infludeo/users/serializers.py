from django.contrib.auth    import get_user_model
from rest_framework         import serializers
from rest_framework_simplejwt.serializers   import TokenObtainPairSerializer


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    User 모델의 시리얼라이저

    기본적인 User 필드만 포함되며, 패스워드는 write_only로 설정되어
    API 응답에 포함되지 않음.

    Attributes:
        id (IntegerField): User ID
        username (CharField): User 이름
        password (CharField): User 비밀번호
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        새로운 User 객체를 생성

        패스워드는 해싱하여 저장.

        Args:
            validated_data (dict): 유효성 검사를 통과한 데이터

        Returns:
            User: 생성된 User 객체
        """
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT 인증을 위한 토큰 시리얼라이저

    기본 JWT 토큰에 User 이름을 추가.

    Methods:
        get_token(cls, user): User 객체를 기반으로 JWT 토큰을 생성
        validate(self, attrs): JWT 토큰을 생성하고, 추가 데이터를 반환
    """
    @classmethod
    def get_token(cls, user):
        """
        User 객체를 기반으로 JWT 토큰을 생성

        Args:
            user (User): User 객체

        Returns:
            Token: JWT 토큰 객체
        """
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        """
        인증 유효성 검사를 수행하고 추가적인 User 정보를 반환.

        Args:
            attrs (dict): 인증 데이터

        Returns:
            dict: 인증된 User 데이터와 토큰 정보를 포함한 응답 데이터
        """
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username,
        }

        return data
