from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class FetchCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["cart_id", "products", "sub_total",
                  "delivery_fees", "tax", "total"]
