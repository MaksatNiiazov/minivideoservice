from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "media_type",
        "source_type",
        "created_at",
    )
    list_filter = ("media_type", "source_type")
    search_fields = ("external_url",)
