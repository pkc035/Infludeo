from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150)
    cash = models.DecimalField(max_digits=10, default=10000)

    def __str__(self):
        return self.username