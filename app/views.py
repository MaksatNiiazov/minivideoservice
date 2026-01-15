from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Media, Category
from .forms import MediaUploadForm



@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = MediaUploadForm(request.POST, request.FILES)

        if form.is_valid():
            media_type = form.cleaned_data["media_type"]
            source_type = form.cleaned_data["source_type"]
            category = form.cleaned_data["category"]
            duration = form.cleaned_data.get("duration")
            external_url = form.cleaned_data.get("external_url")

            # 🔹 ОПТОВАЯ загрузка файлов
            if source_type == Media.SourceType.FILE:
                files = request.FILES.getlist("files")

                for f in files:
                    Media.objects.create(
                        media_type=media_type,
                        source_type=Media.SourceType.FILE,
                        category=category,
                        duration=duration,
                        file=f,
                    )

            # 🔹 Загрузка по ссылке
            elif source_type == Media.SourceType.LINK:
                Media.objects.create(
                    media_type=media_type,
                    source_type=Media.SourceType.LINK,
                    category=category,
                    duration=duration,
                    external_url=external_url,
                )

            return redirect("index")

    else:
        form = MediaUploadForm()

    # 🔹 фильтрация по категории
    category_id = request.GET.get("category")

    items = Media.objects.all().order_by("-created_at")
    if category_id:
        items = items.filter(category_id=category_id)

    return render(
        request,
        "app/index.html",
        {
            "form": form,
            "items": items,
            "categories": Category.objects.all(),
            "selected_category": category_id,
        },
    )


def view_image(request, pk):
    media = get_object_or_404(Media, pk=pk)
    return render(request, "view_image.html", {"media": media})


def view_video(request, pk):
    media = get_object_or_404(Media, pk=pk)
    return render(request, "view_video.html", {"media": media})
