from django import forms
from django.forms.models import construct_instance
from .models import Media


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MediaUploadForm(forms.ModelForm):
    # ⚠️ ВАЖНО: НЕ FileField
    files = forms.Field(
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

        # ⚠️ ТОЛЬКО ТАК
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

    def _post_clean(self):
        exclude = self._get_validation_exclusions()
        self.instance = construct_instance(
            self,
            self.instance,
            self._meta.fields,
            self._meta.exclude,
        )

        files = self.files.getlist("files")
        if (
            self.cleaned_data.get("source_type") == Media.SourceType.FILE
            and files
        ):
            self.instance.file = files[0]
            self.instance.external_url = None

        self.instance.full_clean(exclude=exclude, validate_unique=False)

        if self._validate_unique:
            self.validate_unique()
