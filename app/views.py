from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import Media
from .forms import MediaUploadForm


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("media-upload")
    else:
        form = MediaUploadForm()

    items = Media.objects.all().order_by("-created_at")[:50]
    return render(request, "index.html", {
        "form": form,
        "items": items,
    })
