from rest_framework     import serializers
from decimal            import Decimal
from .models            import Sale
from cards.serializers  import PhotoCardSerializer

class SaleListSerializer(serializers.ModelSerializer):
    photo_card = PhotoCardSerializer()

    class Meta:
        model = Sale
        fields = '__all__'

class SaleDetailSerializer(serializers.ModelSerializer):
    photo_card = PhotoCardSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'photo_card', 'price', 'fee', 'total_price']

    def get_total_price(self, obj):
        return int(obj.price + obj.fee)

class SaleCreateSerializer(serializers.ModelSerializer):
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