from django.urls import path
from .views import index, bot_upload

urlpatterns = [
    path("", index, name="index"),
    path("bot/upload/", bot_upload),
]
