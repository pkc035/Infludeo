from django.db import models
from django.contrib.auth    import get_user_model
from cards.models import PhotoCard

User = get_user_model()

class Sale(models.Model):
    photo_card = models.ForeignKey(PhotoCard, on_delete=models.CASCADE, related_name='sales')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    fee = models.DecimalField(max_digits=10, decimal_places=0)
    state = models.CharField(max_length=20, choices=[('판매중', '판매중'), ('판매완료', '판매완료')], default='판매중')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='buyers')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sellers')
    create_date = models.DateTimeField(auto_now_add=True)
    renewal_date = models.DateTimeField(auto_now=True)
    sold_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.photo_card.name} - {self.state}'