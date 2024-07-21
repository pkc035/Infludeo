from django.db              import models
from django.contrib.auth    import get_user_model
from cards.models           import PhotoCard

User = get_user_model()

class Sale(models.Model):
    """
    Sale 모델

    Attributes:
        photo_card (ForeignKey): 판매하는 포토카드를 참조
        price (DecimalField): 판매 가격
        fee (DecimalField): 수수료
        state (CharField): 판매 상태 ('판매중' 또는 '판매완료')
        buyer (ForeignKey): 구매자를 참조
        seller (ForeignKey): 판매자를 참조
        create_date (DateTimeField): 판매 항목이 생성된 날짜
        renewal_date (DateTimeField): 판매 항목이 수정된 날짜
        sold_date (DateTimeField): 판매가 완료된 날짜
    """
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
        """
        판매 항목의 문자열 표현을 반환.

        Returns:
            str: PhotoCard의 이름과 판매 상태를 포함한 문자열
        """
        return f'{self.photo_card.name} - {self.state}'