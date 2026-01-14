from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from .models import Media


def index(request):
    media_list = Media.objects.order_by("-created_at")
    return render(request, "index.html", {"media_list": media_list})


@csrf_exempt
def bot_upload(request):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)

    if request.headers.get("X-BOT-KEY") != settings.BOT_API_KEY:
        return HttpResponseForbidden("invalid bot key")

    media_type = request.POST.get("media_type")
    source_type = request.POST.get("source_type")

    media = Media(
        media_type=media_type,
        source_type=source_type,
    )

    if source_type == "file":
        media.file = request.FILES.get("file")

    if source_type == "link":
        media.external_url = request.POST.get("external_url")

    media.full_clean()
    media.save()

    return JsonResponse({"status": "ok", "id": media.id})
