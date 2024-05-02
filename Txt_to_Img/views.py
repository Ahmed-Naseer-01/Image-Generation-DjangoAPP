# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from Txt_to_Img.models import GeneratedImage
from Txt_to_Img.serializers import ImageGenerationSerializer, GeneratedImageSerializer
from accounts.renderers import UserRenderer
import base64
import requests


class GenerateImageView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = ImageGenerationSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            print("here is prompt ", prompt)
            API_URL = "https://api-inference.huggingface.co/models/ahmed-naseer/designgen-23k-25k"
            headers = {"Authorization": "Bearer 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"}
 
            payload = {
                "inputs": prompt + "textile design",
            }
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.content
                # Save generated image to database
                user = request.user
                generated_image = GeneratedImage.objects.create(user=user, prompt=prompt)
                print("generated_image proof", generated_image)
                generated_image.image.save(f'{prompt}.jpg', ContentFile(result), save=True)
                
                # Encode image bytes as base64 string
                image_base64 = base64.b64encode(result).decode('utf-8')
                return Response({'image_base64': image_base64}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Failed to generate image. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)


class GeneratedImageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        image = GeneratedImage.objects.all()
        # image = GeneratedImage.objects.get(pk=pk)
        serializer = GeneratedImageSerializer(image, many=True )
        return Response(serializer.data)

    # def get(self, request):
    #     images = GeneratedImage.objects.all()
    #     serializer = GeneratedImageSerializer(images, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = GeneratedImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            image = GeneratedImage.objects.get(pk=pk)
            if image.user == request.user:
                image.delete()
                return Response({'message': 'Image deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You are not allowed to delete this image.'}, status=status.HTTP_403_FORBIDDEN)
        except GeneratedImage.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            image = GeneratedImage.objects.get(pk=pk)
            if image.user == request.user:
                serializer = GeneratedImageSerializer(image, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'You are not allowed to update this image.'}, status=status.HTTP_403_FORBIDDEN)
        except GeneratedImage.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)





















# from rest_framework import status
# # from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from Txt_to_Img.models import GeneratedImage
# from django.core.files.base import ContentFile
# from Txt_to_Img.serializers import ImageGenerationSerializer
# from accounts.renderers import UserRenderer
# from rest_framework.permissions import IsAuthenticated
# import base64
# import requests


# class GenerateImageView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         serializer = ImageGenerationSerializer(data=request.data)
#         if serializer.is_valid():
#             prompt = serializer.validated_data['prompt']
#             API_URL = "https://api-inference.huggingface.co/models/ahmed-naseer/designgen-23k-25k"
#             headers = {"Authorization": "Bearer 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"}
 
#             payload = {
#                 "inputs": prompt,
#             }
#             response = requests.post(API_URL, headers=headers, json=payload)

#             if response.status_code == 200:
#                 result = response.content
#                 # Save generated image to database
#                 user = request.user  # Assuming user is authenticated
#                 generated_image = GeneratedImage.objects.create(user=user, prompt=prompt)
#                 generated_image.image.save(f'{prompt}.jpg', ContentFile(result), save=True)
                
#                 # Encode image bytes as base64 string
#                 image_base64 = base64.b64encode(result).decode('utf-8')
#                 return Response({'image_base64': image_base64}, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Failed to generate image. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

# -------------------------------------------------------------------------------------------------------------------



















# @api_view(['POST'])
# def generate_image(request):
#     if request.method == 'POST':
#         serializer = ImageGenerationSerializer(data=request.data)
#         if serializer.is_valid():
#             prompt = serializer.validated_data['prompt']
#             API_URL = "https://api-inference.huggingface.co/models/ahmed-naseer/designgen-23k-25k"
#             headers = {"Authorization": "Bearer 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"}
 
#             payload = {
#                 "inputs": prompt,
#             }
#             response = requests.post(API_URL, headers=headers, json=payload)

#             if response.status_code == 200:
#                 result = response.content
#                 # Save generated image to database
#                 user = request.user  # Assuming user is authenticated
#                 generated_image = GeneratedImage.objects.create(user=user, prompt=prompt)
#                 generated_image.image.save(f'{prompt}.jpg', ContentFile(result), save=True)
                
#                 # Encode image bytes as base64 string
#                 image_base64 = base64.b64encode(result).decode('utf-8')
#                 return Response({'image_base64': image_base64}, status=status.HTTP_200_OK)
    
#     return Response({'error': 'Failed to generate image. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)