from rest_framework.views import APIView

from homepage.serializers import BannerSerializer, ViewFeaturesMASerializer, ViewFeaturesWASerializer
from common.constants import SUCCESSFULLY_FETCHED_HOMEPAGE_DATA
from exceptions.generic_response import GenericSuccessResponse
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
