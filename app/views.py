from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Media, Category
from .forms import MediaUploadForm


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("files")

            base_data = {
                "media_type": form.cleaned_data["media_type"],
                "source_type": form.cleaned_data["source_type"],
                "category": form.cleaned_data["category"],
                "duration": form.cleaned_data.get("duration"),
            }

            # 🔹 загрузка файлов оптом
            for f in files:
                Media.objects.create(
                    **base_data,
                    file=f,
                )

            # 🔹 загрузка по ссылке (одиночная)
            if base_data["source_type"] == Media.SourceType.LINK:
                Media.objects.create(
                    **base_data,
                    external_url=form.cleaned_data["external_url"],
                )

            return redirect("index")
    else:
        form = MediaUploadForm()

    category_id = request.GET.get("category")
    items = Media.objects.all().order_by("-created_at")
    if category_id:
        items = items.filter(category_id=category_id)

    return render(
        request,
        "index.html",
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
