from django.db import models
from django.core.exceptions import ValidationError


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

    preview = models.ImageField(upload_to="previews/", null=True, blank=True)

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)

    telegram_user_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        has_file = bool(self.file)
        has_url = bool(self.external_url)

        # строго XOR
        if has_file == has_url:
            raise ValidationError("Нужно указать либо file, либо external_url (но не оба).")

        # согласованность source_type
        if self.source_type == self.SourceType.FILE and not has_file:
            raise ValidationError("source_type=file требует file.")
        if self.source_type == self.SourceType.LINK and not has_url:
            raise ValidationError("source_type=link требует external_url.")

        # duration только для video
        if self.media_type == self.MediaType.PHOTO and self.duration is not None:
            raise ValidationError("duration допускается только для video.")
        if self.media_type == self.MediaType.VIDEO and self.duration is not None and self.duration < 0:
            raise ValidationError("duration не может быть отрицательной.")

    def __str__(self):
        return f"{self.media_type} ({self.source_type}) #{self.id}"
