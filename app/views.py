from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Media, Category
from .forms import MediaUploadForm


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = MediaUploadForm()

    category_id = request.GET.get("category")

    items = Media.objects.all().order_by("-created_at")
    if category_id:
        items = items.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(
        request,
        "index.html",
        {
            "form": form,
            "items": items,
            "categories": categories,
            "selected_category": category_id,
        },
    )


def view_image(request, pk):
    media = get_object_or_404(Media, pk=pk)
    return render(request, "view_image.html", {"media": media})