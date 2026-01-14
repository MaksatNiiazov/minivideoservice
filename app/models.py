from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


class Media(models.Model):
    class MediaType(models.TextChoices):
        PHOTO = "photo", "Фото"
        VIDEO = "video", "Видео"

    class SourceType(models.TextChoices):
        FILE = "file", "Файл"
        LINK = "link", "Ссылка"

    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    source_type = models.CharField(max_length=10, choices=SourceType.choices)

    file = models.FileField(upload_to="media/", null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    preview = models.ImageField(upload_to="media/", null=True, blank=True)

    duration = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="media",
    )

    def clean(self):
        has_file = bool(self.file)
        has_url = bool(self.external_url)

        if has_file == has_url:
            raise ValidationError("Нужно указать либо file, либо external_url.")

        if self.media_type == self.MediaType.PHOTO and self.duration:
            raise ValidationError("duration только для видео.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # 🔹 Обрабатываем только новые фото с файлом
        if (
                is_new
                and self.media_type == self.MediaType.PHOTO
                and self.file
        ):
            self._convert_to_webp_and_cleanup()

    def _convert_to_webp_and_cleanup(self):
        original_path = self.file.path

        # Открываем изображение
        img = Image.open(original_path)
        img = img.convert("RGB")

        # Уменьшаем (длинная сторона максимум 1200px)
        img.thumbnail((1200, 1200))

        buffer = BytesIO()
        img.save(
            buffer,
            format="WEBP",
            quality=82,
            method=6,
        )
        buffer.seek(0)

        base_name = os.path.splitext(os.path.basename(original_path))[0]
        preview_name = f"{base_name}.webp"

        # Сохраняем превью
        self.preview.save(
            preview_name,
            ContentFile(buffer.read()),
            save=False,
        )

        # ❌ удаляем оригинальный файл
        self.file.delete(save=False)
        self.file = None

        # сохраняем изменения
        self.save(update_fields=["preview", "file"])


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name
