from django import forms
from .models import Media



class MediaUploadForm(forms.ModelForm):
    files = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"multiple": True}),
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
        files = self.files.getlist("files")
        source_type = cleaned.get("source_type")

        if source_type == Media.SourceType.FILE and not files:
            raise forms.ValidationError("Выбери хотя бы один файл.")

        if source_type == Media.SourceType.LINK and not cleaned.get("external_url"):
            raise forms.ValidationError("Укажи ссылку.")

        return cleaned