from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "LittleLemonAPI"

router = DefaultRouter()
router.register(r"groups/manager/users", ManagerGroupView, basename="manager-group")
router.register(
    r"groups/delivery-crew/users", DeliveryCrewGroupView, basename="delivery-crew-group"
)
router.register(r"category", CategoryView)

urlpatterns = [
    path("", include("djoser.urls")),
] + router.urls
