from django.urls import path
from .views import index, view_image

urlpatterns = [
    path("", index, name="index"),
    path("image/<int:pk>/", view_image, name="view-image"),
]
