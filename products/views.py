from decimal import Decimal
import json
from rest_framework.views import APIView
from django.db.models import Q


from common.constants import (BAD_REQUEST,
                              DATA_ADDED_SUCCESSFULLY, DATA_IS_INVALID,
                              DATA_NOT_FOUND, PRODUCT_IS_ALREADY_RATED,
                              PRODUCT_RATED_SUCCESSFULLY,
                              SUCCESSFULLY_FETCHED_HOMEPAGE_DATA,
                              SUCCESSFULLY_FETCHED_PRODUCT_DETAILS,
                              SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS)

from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from homepage.models import Features

from products.models import ProductRatingModel, ProductReviewModel, Products
from products.serializers import AddProductSerializer, FetchProductRatingSerializer, FetchProductReviewSerializer, ProductRatingSerializer, ProductReviewSerializer, ViewProductsDetailsSerializer, ViewProductsListingSerializer
from products.paginations import CustomPagination

from security.customer_authorization import CustomerJWTAuthentication


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

                # data = {"product_list": view_product_listing_serializer.data,
                #         "product_objects": product_objects,
                #         "total_pages": len(view_product_listing_serializer.data)/3}
                return GenericSuccessResponse(view_product_listing_serializer.data, message=SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS, status=200)

            else:
                return CustomBadRequest(message=BAD_REQUEST)

        except Exception:
            return GenericException(request=request)


class SortAndFilterProducts(APIView):
    @staticmethod
    def get(request):
        try:
            search = request.query_params.get("search")
            sort_type = request.query_params.get("sort_type")
            price_range = request.query_params.get("price_range")
            rating = request.query_params.get("rating")

            if not search:
                return CustomBadRequest(message=BAD_REQUEST)

            priority_products = Products.objects.filter(
                product_name__istartswith=search, is_deleted=False)

            extra_id = priority_products.values_list(
                'product_id', flat=True)

            extra_products = Products.objects.filter(
                product_name__icontains=search, is_deleted=False
            ).exclude(product_id__in=extra_id)

            if price_range:
                price_range = json.loads(price_range)
                min_price = float(price_range[0])
                max_price = float(price_range[1])

                priority_products = priority_products.filter(
                    product_price__gt=min_price, product_price__lt=max_price)
                extra_products = extra_products.filter(
                    product_price__gt=min_price, product_price__lt=max_price)

            if rating:
                priority_products = priority_products.filter(
                    product_rating=rating)
                extra_products = extra_products.filter(
                    product_rating=rating)

            # sorting
            if sort_type == "price_desc":
                priority_products = priority_products.order_by(
                    '-product_price')

                extra_products = extra_products.order_by(
                    '-product_price')

            if sort_type == "price_asc":
                priority_products = priority_products.order_by(
                    'product_price')

                extra_products = extra_products.order_by(
                    'product_price')

            if sort_type == "top_rated":
                priority_products = priority_products.order_by(
                    '-product_rating')

                extra_products = extra_products.order_by(
                    '-product_rating')

            if sort_type == "popularity":
                priority_products = priority_products.order_by(
                    '-product_total_sales')

                extra_products = extra_products.order_by(
                    '-product_total_sales')

            if sort_type == "discount":
                priority_products = priority_products.order_by(
                    '-product_discount')

                extra_products = extra_products.order_by(
                    '-product_discount')

            if not sort_type or sort_type == "":
                priority_products = priority_products

                extra_products = extra_products

            sorted_products = list(
                priority_products) + list(extra_products)

            paginator = CustomPagination()
            paginated_products = paginator.paginate_queryset(
                sorted_products, request)

            view_product_listing_serializer = ViewProductsListingSerializer(
                paginated_products, many=True)

            # data = {"product_list": view_product_listing_serializer.data,
            #         "product_objects": product_objects,
            #         "total_pages": len(view_product_listing_serializer.data)/3}

            return GenericSuccessResponse(view_product_listing_serializer.data, message=SUCCESSFULLY_FETCHED_SEARCHED_PRODUCTS, status=200)

        except Exception:
            return GenericException(request=request)


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
            return GenericException(request=request)

# just for testing purpose


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
                "product_image" not in request.FILES or
                "product_price" not in request.data or request.data["product_price"] == "" or
                "product_arival_date" not in request.data or
                "product_final_price" not in request.data or
                "product_category" not in request.data or
                "product_brand" not in request.data or
                "product_dimension" not in request.data or
                "product_weight" not in request.data or
                "product_color" not in request.data or
                    "additional_specification" not in request.data):

                return CustomBadRequest(message=BAD_REQUEST)
            product_serializer = AddProductSerializer()

            if product_serializer.is_valid():
                product_serializer.save()

                return GenericSuccessResponse(product_serializer.data, message=DATA_ADDED_SUCCESSFULLY, status=201)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Exception:
            return GenericException(request=request)


class ProductRating(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def post(request):
        try:
            if ("product_id" not in request.data or request.data["product_id"] == "" or
                        "product_rating" not in request.data or request.data["product_rating"] == ""
                    ):
                return CustomBadRequest(message=BAD_REQUEST)

            request.data['customer_id'] = request.user.customer_id

            if ProductRatingModel.objects.filter(is_deleted=False, product_id=request.data['product_id'], customer_id=request.data["customer_id"]).exists():
                return CustomBadRequest(message=PRODUCT_IS_ALREADY_RATED)

            product_details = Products.objects.get(
                product_id=request.data["product_id"], is_deleted=False)

            ratings = ProductRatingModel.objects.filter(
                is_deleted=False, product_id=request.data['product_id'])

            total_rating = sum(ratings.values_list(
                'product_rating', flat=True))+int(request.data["product_rating"])

            product_rating = total_rating/(len(ratings)+1)

            if product_rating-int(product_rating) >= 0.5:
                product_rating = int(product_rating)+1
            else:
                product_rating = int(product_rating)

            product_details.product_rating = product_rating

            rating_data = {"product_id": request.data["product_id"],
                           "product_rating": request.data["product_rating"],
                           "product_review": request.data["product_review"],
                           "customer_id": request.data["customer_id"]}

            product_rating_serializer = ProductRatingSerializer(
                data=rating_data)

            if product_rating_serializer.is_valid():

                product_rating_serializer.save()
                product_details.save()

            else:
                CustomBadRequest(message=DATA_IS_INVALID)
            if product_rating_serializer.is_valid():
                product_rating_serializer.save()
            else:
                CustomBadRequest(message=DATA_IS_INVALID)

            return GenericSuccessResponse(message=PRODUCT_RATED_SUCCESSFULLY, status=201)

        except Exception as e:
            return GenericException(request=request)


class ProductsDetails(APIView):

    @staticmethod
    def get(request):
        try:
            product_id = request.query_params.get("product_id")
            if product_id:

                product_details = Products.objects.get(
                    is_deleted=False, product_id=product_id)

                product_ratings = ProductRatingModel.objects.filter(
                    is_deleted=False, product_id=product_id)

                product_reviews = ProductReviewModel.objects.filter(
                    is_deleted=False, product_id=product_id)
                product_physical_details = {"product_brand": product_details.product_brand,
                                            "product_color": product_details.product_color,
                                            "product_weight": product_details.product_weight,
                                            "product_dimension": product_details.product_dimension}

                rating_stats = {"1": len(product_ratings.filter(product_rating=1)),
                                "2": len(product_ratings.filter(product_rating=2)),
                                "3": len(product_ratings.filter(product_rating=3)),
                                "4": len(product_ratings.filter(product_rating=4)),
                                "5": len(product_ratings.filter(product_rating=5))}

                data = {"product_details": ViewProductsDetailsSerializer(product_details).data,
                        "product_physical_details": product_physical_details,
                        "product_ratings": FetchProductRatingSerializer(product_ratings, many=True).data,
                        "number_of_ratings": len(product_ratings),
                        "rating_stats": rating_stats,
                        "product_reviews": FetchProductReviewSerializer(product_reviews, many=True).data,
                        "number_of_reviews": len(product_reviews),
                        }

                return GenericSuccessResponse(data, message=SUCCESSFULLY_FETCHED_PRODUCT_DETAILS, status=200)
            else:
                return CustomBadRequest(message=BAD_REQUEST)
        except Products.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)
