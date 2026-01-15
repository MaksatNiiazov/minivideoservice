from django import forms
from .models import Media


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MediaUploadForm(forms.ModelForm):
    # 🔹 поле ТОЛЬКО для оптовой загрузки
    files = forms.FileField(
        required=False,
        widget=MultipleFileInput(),
        label="Файлы (можно выбрать несколько)",
    )

    class Meta:
        model = Media
        fields = (
            "media_type",
            "source_type",
            "category",
            "external_url",
            "duration",
        )

    def clean(self):
        cleaned = super().clean()

        source_type = cleaned.get("source_type")
        external_url = cleaned.get("external_url")

        # ⚠️ ВАЖНО: файлы берём ТОЛЬКО так
        files = self.files.getlist("files")

        if source_type == Media.SourceType.FILE:
            if not files:
                raise forms.ValidationError(
                    "Нужно выбрать хотя бы один файл."
                )

        if source_type == Media.SourceType.LINK:
            if not external_url:
                raise forms.ValidationError(
                    "Нужно указать external URL."
                )

        return cleaned
