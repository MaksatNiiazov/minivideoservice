from django.db import models
from django.core.exceptions import ValidationError


class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("photo", "Фото"),
        ("video", "Видео"),
    )

    SOURCE_TYPE_CHOICES = (
        ("file", "Файл"),
        ("link", "Ссылка"),
    )

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES)

    file = models.FileField(upload_to="media/", null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.source_type == "file" and not self.file:
            raise ValidationError("Для source_type=file обязателен файл")

        if self.source_type == "link" and not self.external_url:
            raise ValidationError("Для source_type=link обязательна ссылка")

        if self.file and self.external_url:
            raise ValidationError("Можно указать либо файл, либо ссылку")

    def __str__(self):
        return f"{self.media_type} ({self.source_type})"
