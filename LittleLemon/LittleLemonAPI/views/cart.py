from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins
from ..utils import DrfRequest
from ..permissions import IsCustomer
from ..models import Cart
from ..serializers import CartInputSerializer, CartRemoveSerializer, CartViewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.throttling import ScopedRateThrottle
from django.db import transaction


class CartView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CartViewSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    throttle_scope = "cart"

    def get_throttles(self):
        if self.request.method == "POST":
            return [ScopedRateThrottle()]
        return []

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get(self, request):
        return self.list(request)

    @transaction.atomic
    def post(self, request: DrfRequest):
        serializer = CartInputSerializer(
            data=request.data, context={"user": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        menu_item = serializer.validated_data["menu_item"]
        quantity = serializer.validated_data["quantity"]
        unit_price = menu_item.price
        cart, created = Cart.objects.update_or_create(
            user=request.user,
            menu_item=menu_item,
            defaults={
                "quantity": quantity,
                "unit_price": unit_price,
                "price": Cart.compute_price(unit_price, quantity),
            },
        )

        if created:
            message = "Item successfully added to cart"
            status_code = status.HTTP_201_CREATED
        else:
            message = "Cart item quantity updated"
            status_code = status.HTTP_200_OK

        return Response(
            {"message": message, "result": CartViewSerializer(cart).data},
            status=status_code,
        )

    def delete(self, request: DrfRequest):
        if "menu_item" in request.data:
            serializer = CartRemoveSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            menu_item_id = serializer.validated_data["menu_item"]

            cart = get_object_or_404(Cart, user=request.user, menu_item_id=menu_item_id)
            cart.delete()
            return Response({"message": "Item removed from cart"})
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response({"message": "All items removed from cart"})
