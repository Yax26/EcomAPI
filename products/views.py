from decimal import Decimal
from rest_framework.views import APIView
from django.db.models import Q


from common.constants import BAD_REQUEST, DATA_ADDED_SUCCESSFULLY, DATA_IS_INVALID, SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS

from exceptions.generic import CustomBadRequest
from exceptions.generic_response import GenericSuccessResponse

from homepage.models import Features

from products.models import Products
from products.serializers import AddProductSerializer, ViewProductsListingSerializer
from products.paginations import CustomPagination


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

                products = list(priority_products) + list(extra_products)

                paginator = CustomPagination()
                paginated_products = paginator.paginate_queryset(
                    products, request)

                view_product_listing_serializer = ViewProductsListingSerializer(
                    paginated_products, many=True)

                return GenericSuccessResponse(view_product_listing_serializer.data, message=SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS, status=200)

            serialized_products = ViewProductsListingSerializer(
                products, many=True)

            return GenericSuccessResponse(serialized_products.data, message=SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, status=200)

        except Exception:
            return GenericSuccessResponse()


class FeaturedProducts(APIView):
    @staticmethod
    def get(request):
        try:

            feature_id = request.query_params.get("feature_id")
            feature = Features.objects.get(feature_id=feature_id)

            if feature.max_price:
                products = Products.objects.filter(
                    product_price__lte=Decimal(feature.max_price), is_deleted=False).order_by('product_price')

            if feature.min_price:
                products = Products.objects.filter(
                    product_price__gte=Decimal(feature.min_price), is_deleted=False).order_by('-product_price')

            if feature.max_discount:
                products = Products.objects.filter(
                    product_discount__lte=Decimal(feature.max_discount), is_deleted=False).order_by('-product_discount')

            if feature.min_discount:
                products = Products.objects.filter(
                    product_discount__gte=Decimal(feature.min_discount), is_deleted=False).order_by('-product_discount')

            if feature.arrival_date:
                products = Products.objects.filter(
                    product_arival_date__gte=feature.arrival_date, is_deleted=False).order_by('-product_arival_date')

            if feature.category_id:
                products = Products.objects.filter(
                    product_category=feature.category_id, is_deleted=False)

            if feature.total_sales:
                products = Products.objects.filter(
                    product_total_sales__gte=feature.total_sales, is_deleted=False).order_by('-product_total_sales')

            if feature.feature_keywords:
                products = Products.objects.filter(
                    Q(product_keywords__icontains=feature.feature_keywords) |
                    Q(product_name__icontains=feature.feature_keywords), is_deleted=False)

            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(
                products, request)
            serialized_products = ViewProductsListingSerializer(
                paginated_products, many=True)

            return GenericSuccessResponse(serialized_products.data, message=SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, status=200)

        except Exception:
            return GenericSuccessResponse()


class AddProductData(APIView):

    @staticmethod
    def post(request):
        try:
            print("check here 1")
            # if ("product_name" not in request.data or request.data["product_name"] == "" or
            #     "product_keywords" not in request.data or
            #     "product_description" not in request.data or
            #     "product_rating" not in request.data or
            #     "product_discount" not in request.data or
            #     "product_available_quantity" not in request.data or request.data["product_available_quantity"] == "" or
            #     "product_image" not in request.data or
            #     "product_price" not in request.data or request.data["product_price"] == "" or
            #     "product_arival_date" not in request.data or
            #     "product_final_price" not in request.data or
            #         "product_category" not in request.data):

            #     return CustomBadRequest(message=BAD_REQUEST)
            print("check here 2")
            product_serializer = AddProductSerializer(data=request.data)

            if product_serializer.is_valid(raise_exception=True):
                print("check here 3")
                product_serializer.save()
                
                return GenericSuccessResponse(product_serializer.data, message=DATA_ADDED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Exception:
            return GenericSuccessResponse()
