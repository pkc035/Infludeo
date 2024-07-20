from rest_framework import serializers
from .models        import PhotoCard

class PhotoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoCard
        fields = '__all__'