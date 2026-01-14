from django import forms
from .models import Media


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ("media_type", "source_type", "file", "external_url", "duration")

    def clean(self):
        cleaned = super().clean()
        media_type = cleaned.get("media_type")
        source_type = cleaned.get("source_type")
        file = cleaned.get("file")
        external_url = cleaned.get("external_url")
        duration = cleaned.get("duration")

        has_file = bool(file)
        has_url = bool(external_url)

        if has_file == has_url:
            raise forms.ValidationError("Укажи либо файл, либо ссылку (одно из двух).")

        if source_type == Media.SourceType.FILE and not has_file:
            raise forms.ValidationError("Выбран 'Файл', но файл не загружен.")
        if source_type == Media.SourceType.LINK and not has_url:
            raise forms.ValidationError("Выбрана 'Ссылка', но ссылка пустая.")

        if media_type == Media.MediaType.PHOTO and duration not in (None, ""):
            raise forms.ValidationError("Для фото длительность не нужна.")
        return cleaned
