from django.urls import path
from Txt_to_Img.views import GenerateImageView, GeneratedImageView


urlpatterns = [
    path('generate/', GenerateImageView.as_view(), name='generate_image'),
    path('images/', GeneratedImageView.as_view(), name='list_create_images'),
    path('images/<int:pk>/', GeneratedImageView.as_view(), name='retrieve_update_delete_image'),
]
