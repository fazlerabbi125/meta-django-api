from rest_framework import serializers
from .models import *


class CartInputSerializer(serializers.ModelSerializer):
    def validate(self, attrs: dict):
        if (
            attrs.get("menu_item")
            and not MenuItem.objects.filter(id=attrs["menu_item"]).exists()
        ):
            raise serializers.ValidationError("Menu item does not exist")

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
        fields = "__all__"
        read_only_fields = ["user"]


class CartRemoveSerializer(serializers.Serializer):
    menu_item = serializers.IntegerField()


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
