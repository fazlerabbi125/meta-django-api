from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from ..utils import GroupEnum, DrfRequest, ConflictFound
from ..permissions import IsManager
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404


class ManagerGroupView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
        IsManager | IsAdminUser,
    ]
    queryset = User.objects.filter(groups__name=GroupEnum.MANAGER.value)
    lookup_url_kwarg = "userId"

    def create(self, request: DrfRequest):
        username = request.data.get("username")
        if not username:
            raise exceptions.ValidationError(detail="Username is required")
        user = get_object_or_404(User, username=username)
        if user.groups.filter(name=GroupEnum.MANAGER.value).exists():
            raise ConflictFound(detail="User is already in the manager group")
        group = get_object_or_404(Group, name=GroupEnum.MANAGER.value)
        group.user_set.add(user)
        return Response(
            {"message": "User successfully added to the manager group"},
            status.HTTP_201_CREATED,
        )

    def destroy(self, request: DrfRequest, userId):
        user = get_object_or_404(User, id=userId)
        if not user.groups.filter(name=GroupEnum.MANAGER.value).exists():
            raise ConflictFound(detail="User is already not in the manager group")
        group = get_object_or_404(Group, name=GroupEnum.MANAGER.value)
        group.user_set.remove(user)
        return Response(
            {"message": "User successfully removed from the manager group"},
        )


class DeliveryCrewGroupView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    queryset = User.objects.filter(groups__name=GroupEnum.DELIVERY_CREW.value)
    lookup_url_kwarg = "userId"

    def create(self, request: DrfRequest):
        username = request.data.get("username")
        if not username:
            raise exceptions.ValidationError(detail="Username is required")
        user = get_object_or_404(User, username=username)
        if user.groups.filter(name=GroupEnum.DELIVERY_CREW.value).exists():
            raise ConflictFound(detail="User is already in the delivery crew group")
        group = get_object_or_404(Group, name=GroupEnum.DELIVERY_CREW.value)
        group.user_set.add(user)
        return Response(
            {"message": "User successfully added to the delivery crew group"},
            status.HTTP_201_CREATED,
        )

    def destroy(self, request: DrfRequest, userId):
        user = get_object_or_404(User, id=userId)
        if not user.groups.filter(name=GroupEnum.DELIVERY_CREW.value).exists():
            raise ConflictFound(detail="User is already not in the delivery crew group")
        group = get_object_or_404(Group, name=GroupEnum.DELIVERY_CREW.value)
        group.user_set.remove(user)
        return Response(
            {"message": "User successfully removed from the delivery crew group"},
        )
