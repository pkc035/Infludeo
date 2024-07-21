from rest_framework     import serializers
from decimal            import Decimal
from .models            import Sale
from cards.serializers  import PhotoCardSerializer

class SaleListSerializer(serializers.ModelSerializer):
    """
    판매 항목의 목록 시리얼라이저

    Sale 모델과 PhotoCard 모델의 필드를 포함하여,
    JSON 데이터로 변환하거나 JSON 데이터를 모델 인스턴스로 변환.

    Attributes:
        photo_card (PhotoCardSerializer): PhotoCard 직렬화
    """
    photo_card = PhotoCardSerializer()

    class Meta:
        model = Sale
        fields = '__all__'

class SaleDetailSerializer(serializers.ModelSerializer):
    """
    판매 항목의 세부 사항 시리얼라이저

    Sale 모델과 PhotoCard 모델의 필드를 포함하여,
    JSON 데이터로 변환하거나 JSON 데이터를 모델 인스턴스로 변환.

    Attributes:
        photo_card (PhotoCardSerializer): PhotoCard 직렬화
        total_price (SerializerMethodField): 가격과 수수료의 합계를 반환
    """
    photo_card = PhotoCardSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'photo_card', 'price', 'fee', 'total_price']

    def get_total_price(self, obj):
        """
        가격과 수수료의 합계를 계산하여 반환.

        Args:
            obj (Sale): Sale 모델 인스턴스

        Returns:
            int: 가격과 수수료의 합계
        """
        return int(obj.price + obj.fee)

class SaleCreateSerializer(serializers.ModelSerializer):
    """
    판매 항목을 생성하기 위한 시리얼라이저

    이 시리얼라이저는 Sale 모델의 필드를 포함하여,
    판매 항목의 생성과 검증을 담당.
    """
    class Meta:
        model = Sale
        fields = ['photo_card', 'price']

    def validate(self, attrs):
        attrs['fee'] = attrs['price'] * Decimal('0.1')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['seller'] = request.user
        return super().create(validated_data)