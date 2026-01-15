from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import Media, Category
from .forms import MediaUploadForm
from django.core.paginator import Paginator


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

    # ---------- ФИЛЬТР ----------
    category_id = request.GET.get("category")
    qs = Media.objects.all().order_by("-created_at")

    if category_id:
        qs = qs.filter(category_id=category_id)

    # ---------- ПАГИНАЦИЯ ----------
    paginator = Paginator(qs, 10)  # 🔥 по 10 элементов
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "form": form,
            "items": page_obj,  # ⚠️ теперь это Page, не QuerySet
            "page_obj": page_obj,
            "paginator": paginator,
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
