from rest_framework.views import APIView

from common.constants import BAD_REQUEST, DATA_ADDED_SUCCESSFULLY, DATA_IS_INVALID, SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS
from exceptions.generic import CustomBadRequest
from exceptions.generic_response import GenericSuccessResponse
from products.models import Products
from products.serializers import AddProductSerializer, ViewProductsListingSerializer


class SearchedProducts(APIView):
    @staticmethod
    def get(request):
        try:
            search = request.query_params.get("search")

            if search:

                priority_products = Products.objects.filter(
                    product_name__istartswith=search, is_deleted=False)

                extra_id = priority_products.values_list(
                    'product_id', flat=True)

                extra_products = Products.objects.filter(
                    product_name__icontains=search, is_deleted=False
                ).exclude(product_id__in=extra_id)

                products = [*priority_products, *extra_products]

                view_product_listing_serializer = ViewProductsListingSerializer(
                    products, many=True)

                return GenericSuccessResponse(view_product_listing_serializer.data, message=SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS, status=200)

            serialized_products = ViewProductsListingSerializer(
                products, many=True)

            return GenericSuccessResponse(serialized_products.data, message=SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, status=200)

        except Exception:
            return GenericSuccessResponse()


class AddProductData(APIView):

    @staticmethod
    def post(request):
        try:

            if ("product_name" not in request.data or request.data["product_name"] == "" or
                "product_keywords" not in request.data or
                "product_description" not in request.data or
                "product_rating" not in request.data or
                "product_discount" not in request.data or
                "product_available_quantity" not in request.data or request.data["product_available_quantity"] == "" or
                "product_image" not in request.data or
                "product_price" not in request.data or request.data["product_price"] == "" or
                "product_arival_date" not in request.data or
                "product_final_price" not in request.data or
                    "product_category" not in request.data):

                return CustomBadRequest(message=BAD_REQUEST)

            product_serializer = AddProductSerializer(data=request.data)

            if product_serializer.is_valid():

                product_serializer.save()
                return GenericSuccessResponse(product_serializer.data, message=DATA_ADDED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Exception:
            return GenericSuccessResponse()
