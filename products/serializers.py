from rest_framework import serializers

from products.models import Products


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


class ViewProductsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["product_id",
                  "product_name",
                  "product_rating",
                  "product_discount",
                  "product_image",
                  "product_price",
                  "product_final_price",
                  "product_category", ]

        read_only_fields = fields
