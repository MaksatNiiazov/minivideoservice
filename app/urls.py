from django.urls import path
from .views import index, view_image, view_video

urlpatterns = [
    path("", index, name="index"),
    path("image/<int:pk>/", view_image, name="view-image"),
    path("video/<int:pk>/", view_video, name="view-video"),
]
