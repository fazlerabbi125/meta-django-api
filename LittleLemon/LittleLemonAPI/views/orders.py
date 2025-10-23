from rest_framework.response import Response
from rest_framework import viewsets, exceptions, status, mixins
from rest_framework.permissions import IsAuthenticated
from ..models import Order, OrderItem, Cart
from ..serializers import (
    CustomerOrderViewSerializer,
    OrderSerializer,
    ManagerOrderUpdateSerializer,
    DeliveryCrewOrderUpdateSerializer,
)
from ..permissions import IsManager, IsCustomer, IsDeliveryCrew
from ..utils import CustomPageNumberPagination, GroupEnum, DrfRequest
from rest_framework.throttling import ScopedRateThrottle
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime

class OrderView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    lookup_url_kwarg = "orderId"
    pagination_class = CustomPageNumberPagination
    throttle_scope = "orders"
    permission_classes = [IsAuthenticated, IsManager | IsDeliveryCrew | IsCustomer]
    ordering_fields = ["total", "date"]

    def get_throttles(self):
        if self.action not in ("list", "retrieve"):
            return [ScopedRateThrottle()]
        return []

    def get_permissions(self):
        match self.action:
            case "create":
                self.permission_classes = [IsAuthenticated, IsCustomer]
            case "update" | "destroy":
                self.permission_classes = [IsAuthenticated, IsManager]
            case "partial_update":
                self.permission_classes = [IsAuthenticated, IsManager | IsDeliveryCrew]
        return super().get_permissions()

    def get_queryset(self):
        query_params:dict = self.request.query_params
        if self.request.user.groups.filter(name=GroupEnum.MANAGER.value).exists():
            filter_dict = dict()
            if "status" in query_params:
                if query_params["status"].lower() == "delivered":
                    filter_dict["status"] = True
                elif query_params["status"].lower() == "pending":
                    filter_dict["status"] = False
            if "date" in query_params:
                try:
                    filter_dict["date"] = datetime.strptime(query_params["date"], "%Y-%m-%d").date()
                except ValueError:
                    pass
            if filter_dict:
                return Order.objects.filter(**filter_dict)
            return Order.objects.all()
        elif self.request.user.groups.filter(
            name=GroupEnum.DELIVERY_CREW.value
        ).exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            if not self.request.user.groups.exists():
                return CustomerOrderViewSerializer
            return OrderSerializer
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request: DrfRequest):
        carts = Cart.objects.select_related("menu_item").filter(user=request.user)
        if not carts.exists():
            raise exceptions.ValidationError(
                "Your cart is empty. Please add items to your cart before placing an order."
            )
        total = sum(item.price for item in carts)
        order = Order.objects.create(
            user=request.user,
            total=total,
        )
        for item in carts:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price,
            )
        carts.delete()
        return Response(
            {
                "message": "Your order has been placed.",
                "result": CustomerOrderViewSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request: DrfRequest, orderId):
        order = get_object_or_404(Order, id=orderId)
        order.delete()
        return Response(
            {"message": "Order has been deleted."},
            status=status.HTTP_200_OK,
        )

    def update(self, request: DrfRequest, orderId):
        order = get_object_or_404(Order, id=orderId)
        serializer = ManagerOrderUpdateSerializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()
        return Response(
            {
                "message": "Order has been updated.",
                "result": OrderSerializer(updated_order).data,
            },
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request: DrfRequest, orderId):
        order = get_object_or_404(Order, id=orderId)
        if request.user.groups.filter(name=GroupEnum.DELIVERY_CREW.value).exists():
            serializer = DeliveryCrewOrderUpdateSerializer(
                order, data=request.data, partial=True
            )
        else:
            serializer = ManagerOrderUpdateSerializer(
                order, data=request.data, partial=True
            )
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()
        return Response(
            {
                "message": "Order has been partially updated.",
                "result": OrderSerializer(updated_order).data,
            },
            status=status.HTTP_200_OK,
        )
