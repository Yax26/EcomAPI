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


class ViewProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["product_id",
                  "product_name",
                  "product_description",
                  "product_rating",
                  "product_discount",
                  "product_image",
                  "product_price",
                  "product_final_price",
                  "product_brand",
                  "product_dimension",
                  "product_weight",
                  "product_color",
                  "additional_specification"]
        read_only_fields = fields


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRatingModel
        fields = "__all__"


class FetchProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRatingModel
        fields = ["product_rating_id", "product_rating"]
        read_only_fields = fields


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReviewModel
        fields = "__all__"


class FetchProductReviewSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = ProductReviewModel
        fields = ["product_review_id", "product_review",
                  "customer_id", "updated_at"]
        read_only_fields = fields

    def get_updated_at(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime('%B %d, %Y')
        return None
