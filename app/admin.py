from django.contrib import admin
from .models import Media, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "media_type", "source_type", "category", "created_at")
    list_filter = ("media_type", "source_type", "category")
    search_fields = ("id",)
    readonly_fields = ("created_at",)
