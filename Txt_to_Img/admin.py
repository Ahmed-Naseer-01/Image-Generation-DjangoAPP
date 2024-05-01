from django.contrib import admin
from Txt_to_Img.models import GeneratedImage


@admin.register(GeneratedImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'prompt', 'created_at')
    # search_fields = ('user__name', 'caption')