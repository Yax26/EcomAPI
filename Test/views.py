from rest_framework.views import APIView

from exceptions.generic_response import GenericSuccessResponse


# Create your views here.

class TestAPI(APIView):
    @staticmethod
    def get(request):

        return GenericSuccessResponse(message='Testing successful', status=200)
