from django import forms
from .models import Media


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MediaUploadForm(forms.ModelForm):
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
        files = self.files.getlist("files")

        if source_type == Media.SourceType.FILE and not files:
            raise forms.ValidationError("Выберите хотя бы один файл.")

        if source_type == Media.SourceType.LINK and not cleaned.get("external_url"):
            raise forms.ValidationError("Укажите ссылку.")

        return cleaned
