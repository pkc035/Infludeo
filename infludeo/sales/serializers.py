from rest_framework import serializers
from .models import Sale
from cards.serializers import PhotoCardSerializer

class SaleListSerializer(serializers.ModelSerializer):
    photo_card = PhotoCardSerializer()

    class Meta:
        model = Sale
        fields = ['id', 'photo_card', 'price']

class SaleDetailSerializer(serializers.ModelSerializer):
    photo_card = PhotoCardSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'photo_card', 'price', 'fee', 'total_price']

    def get_total_price(self, obj):
        return obj.price + obj.fee

class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['photo_card', 'price', 'seller']

    def validate(self, attrs):
        attrs['fee'] = attrs['price'] * 0.1
        return attrs
