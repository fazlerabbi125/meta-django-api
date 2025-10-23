from rest_framework import permissions
from .utils import GroupEnum, DrfRequest
from .models import Order

class IsManager(permissions.BasePermission):
    # message: str
    # code: int # Default 403

    def has_permission(self, request: DrfRequest, view):
        return bool(
            request.user
            and request.user.groups.filter(name=GroupEnum.MANAGER.value).exists()
        )


class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request: DrfRequest, view):
        return bool(
            request.user
            and request.user.groups.filter(name=GroupEnum.DELIVERY_CREW.value).exists()
        )
    def has_object_permission(self, request: DrfRequest, view, obj):
        if isinstance(obj, Order):
            return obj.delivery_crew == request.user
        return True


class IsCustomer(permissions.BasePermission):    
    def has_permission(self, request: DrfRequest, view):
        return bool(request.user and not request.user.groups.exists())
    
    def has_object_permission(self, request: DrfRequest, view, obj):
        if type(obj) == Order:
            return obj.user == request.user
        return True
