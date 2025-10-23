from rest_framework import permissions
from .utils import GroupEnum, DrfRequest


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


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request: DrfRequest, view):
        return bool(request.user and request.user.groups.count() == 0)
