from rest_framework import serializers
from .models        import PhotoCard

class PhotoCardSerializer(serializers.ModelSerializer):
    """
    PhotoCard 모델 시리얼라이저

    PhotoCard 모델의 모든 필드를 포함하여,
    JSON 데이터로 변환하거나 JSON 데이터를 모델 인스턴스로 변환.
    """
    class Meta:
        model = PhotoCard
        fields = '__all__'