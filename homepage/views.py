from rest_framework.views import APIView


from common.constants import BAD_REQUEST, DATA_IS_INVALID, HOMEPAGE_DATA_ADDED_SUCCESSFULLY, SUCCESSFULLY_FETCHED_HOMEPAGE_DATA

from exceptions.generic import CustomBadRequest
from exceptions.generic_response import GenericSuccessResponse

from homepage.serializers import AddFeaturesSerializer, BannerSerializer, ViewFeaturesMASerializer, ViewFeaturesWASerializer
from homepage.models import Banner, Features


class HomePageMA(APIView):

    @staticmethod
    def get(request):
        try:
            features = Features.objects.filter(is_deleted=False)
            banner = Banner.objects.filter(is_deleted=False)

            data = {'features':
                    ViewFeaturesMASerializer(features, many=True).data, 'banner': BannerSerializer(banner, many=True).data}

            return GenericSuccessResponse(data, message=SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, status=200)
        except Exception:
            return GenericSuccessResponse()


class HomePageWA(APIView):

    @staticmethod
    def get(request):
        try:
            features = Features.objects.filter(is_deleted=False)
            banner = Banner.objects.filter(is_deleted=False)

            data = {'features':
                    ViewFeaturesWASerializer(features, many=True).data, 'banner': BannerSerializer(banner, many=True).data}

            return GenericSuccessResponse(data, message=SUCCESSFULLY_FETCHED_HOMEPAGE_DATA, status=200)
        except Exception:

            return GenericSuccessResponse()


class AddFeatureData(APIView):
    @staticmethod
    def post(request):
        try:
            if ("feature_title" not in request.data or request.data["feature_title"] == "" or
                "feature_keywords" not in request.data or
                "category_id" not in request.data or
                "total_sales" not in request.data or
                "max_price" not in request.data or
                "min_price" not in request.data or
                "max_discount" not in request.data or
                "min_discount" not in request.data or
                "arrival_date" not in request.data or
                "feature_image1" not in request.data or request.data["feature_image1"] == "" or
                "feature_image2" not in request.data or request.data["feature_image2"] == "" or
                "feature_image3" not in request.data or request.data["feature_image3"] == "" or
                    "feature_image4" not in request.data or request.data["feature_image4"] == ""):

                return CustomBadRequest(message=BAD_REQUEST)

            add_features_serializer = AddFeaturesSerializer(
                data=request.data)

            if add_features_serializer.is_valid():
                add_features_serializer.save()

                return GenericSuccessResponse(message=HOMEPAGE_DATA_ADDED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Exception:

            return GenericSuccessResponse()


class AddBannerData(APIView):
    @staticmethod
    def post(request):
        try:
            if ("banner_title" not in request.data or request.data["banner_title"] == "" or
                "banner_keyword" not in request.data or
                "banner_image" not in request.data or request.data["banner_image"] == "" or
                    "banner_description" not in request.data or
                    "feature_id" not in request.data):

                return CustomBadRequest(message=BAD_REQUEST)

            add_banner_serializer = BannerSerializer(data=request.data)

            if add_banner_serializer.is_valid():
                add_banner_serializer.save()

                return GenericSuccessResponse(message=HOMEPAGE_DATA_ADDED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)
        except Exception:

            return GenericSuccessResponse()
