from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    cash = models.DecimalField(max_digits=10, decimal_places=0, default=10000)