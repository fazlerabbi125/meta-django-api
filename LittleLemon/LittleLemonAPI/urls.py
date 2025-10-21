from django.urls import path, include
from .views import menu_items

app_name = "LittleLemonAPI"

urlpatterns = [
    path("", include("djoser.urls")),
]
