from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Category, MenuItem
from ..permissions import IsManager
from ..serializers import CategorySerializer, MenuItemSerializer
from ..utils import CustomPageNumberPagination

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


class MenuItemView(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    lookup_url_kwarg = "menuItem"
    pagination_class = CustomPageNumberPagination
    search_fields = ["title", "=category__title"]
    ordering_fields = ["price"]

    def get_permissions(self):
        if self.action in (
            "retrieve",
            "list",
        ):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        query_params = self.request.query_params
        if not query_params:
            return MenuItem.objects.select_related("category").all()
        filter_dict = dict()
        if "category" in query_params:
            filter_dict["category__title__iexact"] = query_params["category"]
        if "title" in query_params:
            filter_dict["title__icontains"] = query_params["title"]
        if "featured" in query_params:
            if query_params["featured"].lower() == "true":
                filter_dict["featured"] = True
            elif query_params["featured"].lower() == "false":
                filter_dict["featured"] = False
        return MenuItem.objects.select_related("category").filter(**filter_dict)
