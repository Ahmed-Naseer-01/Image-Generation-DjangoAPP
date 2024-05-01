# serializers.py
from rest_framework import serializers
from Txt_to_Img.models import GeneratedImage


class ImageGenerationSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=100)


class GeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedImage
        fields = ['id', 'prompt', 'image', 'created_at']
        extra_kwargs = {'prompt': {'required': False}, 'image': {'required': False}}

