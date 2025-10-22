from rest_framework.response import Response
from rest_framework import status, generics, permissions, exceptions
from ..utils import DrfRequest
from ..permissions import IsCustomer
from ..models import Cart, MenuItem
from ..serializers import CartInputSerializer, CartRemoveSerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class CartView(generics.GenericAPIView):
    serializer_class = CartInputSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def post(self, request: DrfRequest):
        serializer = CartInputSerializer(
            data=request.data, context={"user": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {"message": "Item already in cart"}, status.HTTP_409_CONFLICT
            )
        return Response(
            {"message": "Item successfully added to cart"}, status.HTTP_201_CREATED
        )

    def delete(self, request: DrfRequest):
        if "menu_item" in request.data:
            serializer = CartRemoveSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            menu_item = serializer.data["menu_item"]
            if not MenuItem.objects.filter(id=menu_item).exists():
                raise exceptions.ParseError(detail="Menu item does not exist")
            cart = get_object_or_404(Cart, user=request.user, menu_item=menu_item)
            cart.delete()
            return Response({"message": "Item removed from cart"})
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response({"message": "All Items removed from cart"})
