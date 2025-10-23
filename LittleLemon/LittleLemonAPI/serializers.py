from rest_framework import serializers
from .models import *


class CartInputSerializer(serializers.ModelSerializer):
    """
    Method responsibilities:
    - to_internal_value(): Converts and transforms field values from the input data itself.
                           Use this for computing/deriving new fields based on other input fields
                           (e.g., calculating price from unit_price and quantity).
    - validate(): Handles business logic validation and assigns context-based values
                  (e.g., user from request context).
    """

    def validate(self, attrs: dict):
        menu_item = attrs.get("menu_item")
        if not menu_item:
            raise serializers.ValidationError("Menu item is required")

        attrs["unit_price"] = menu_item.price

        if self.context.get("user"):
            attrs["user"] = self.context["user"]

        return attrs

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if "unit_price" in ret or "quantity" in ret:
            if self.instance:
                unit_price = ret.get("unit_price", self.instance.unit_price)
                quantity = ret.get("quantity", self.instance.quantity)
            else:
                unit_price = ret.get("unit_price", 0)
                quantity = ret.get("quantity", 0)

            ret["price"] = Cart.compute_price(unit_price, quantity)
        return ret

    class Meta:
        model = Cart
        fields = ["menu_item", "quantity"]
        read_only_fields = ["user", "unit_price", "price"]


class CartRemoveSerializer(serializers.Serializer):
    menu_item = serializers.IntegerField()


class CartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if "title" in ret and (
            not self.instance or self.instance.title != ret["title"]
        ):
            ret["slug"] = Category.generate_slug(ret["title"])
        return ret

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["slug"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = MenuItem
        fields = "__all__"


class CustomerOrderViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["delivery_crew"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ManagerOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status", "delivery_crew"]


class DeliveryCrewOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
