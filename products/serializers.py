from rest_framework import serializers

from products.models import ProductRatingModel, ProductReviewModel, Products


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
                  ]

        read_only_fields = fields


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRatingModel
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewModel
        fields = "__all__"
