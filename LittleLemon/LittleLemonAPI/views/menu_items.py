from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from ..models import Category
from ..utils import DrfRequest
from ..permissions import IsManager
from ..serializers import CategorySerializer
from django.shortcuts import get_object_or_404


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in (
            "list",
            "retrieve",
        ):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


# class ManagerGroupView(mixins.ListModelMixin, viewsets.GenericViewSet):
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated, IsManager]
#     queryset = User.objects.filter(groups__name=GroupEnum.MANAGER.value)
#     lookup_url_kwarg = "userId"

#     def create(self, request: DrfRequest):
#         username = request.data.get("username")
#         if not username:
#             raise exceptions.ValidationError(detail="Username is required")
#         user = get_object_or_404(User, username=username)
#         if user.groups.filter(name=GroupEnum.MANAGER.value).exists():
#             raise exceptions.ParseError(detail="User is already a manager")
#         group = get_object_or_404(Group, name=GroupEnum.MANAGER.value)
#         group.user_set.add(user)
#         return Response(
#             {"message": "User successfully added to manager role"},
#             status.HTTP_201_CREATED,
#         )

#     def destroy(self, request: DrfRequest, userId):
#         user = get_object_or_404(User, id=userId)
#         if not user.groups.filter(name=GroupEnum.MANAGER.value).exists():
#             raise exceptions.ParseError(detail="User is already not a manager")
#         group = get_object_or_404(Group, name=GroupEnum.MANAGER.value)
#         group.user_set.remove(user)
#         return Response(
#             {"message": "User successfully removed from manager role"},
#         )
