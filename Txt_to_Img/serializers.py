# serializers.py
from rest_framework import serializers
from Txt_to_Img.models import GeneratedImage


class ImageGenerationSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=100)


# class GeneratedImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GeneratedImage
#         fields = ['id', 'prompt', 'image', 'created_at']
#         extra_kwargs = {'prompt': {'required': False}, 'image': {'required': False}}

class GeneratedImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        # Assuming 'image' is the field in your model storing the image path
        
        return obj.image.url 

    class Meta:
        model = GeneratedImage
        fields = ['id', 'prompt', 'image', 'created_at']
        extra_kwargs = {'prompt': {'required': False}, 'image': {'required': False}}

