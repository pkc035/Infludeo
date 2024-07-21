from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    User 모델

    기본 Django User 모델(AbstractUser)을 확장하여, 
    추가적인 필드인 `cash`를 포함합니다. `cash`는 User의 잔액을 나타내며,
    `DecimalField`를 사용하여 소수점 없이 정수로만 저장.

    Attributes:
        cash (DecimalField): User의 잔액(기본값 10000)
    """
    cash = models.DecimalField(max_digits=10, decimal_places=0, default=10000)