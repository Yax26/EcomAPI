from rest_framework.views import APIView


from common.constants import (ADDRESS_INFO_UPDATED_SUCCESSFULLY,
                              BAD_REQUEST, CITY_DOES_NOT_EXISTS,
                              COUNTRY_DOES_NOT_EXISTS,
                              DATA_IS_INVALID,
                              DATA_NOT_FOUND,
                              PERSONAL_INFO_UPDATED_SUCCESSFULLY,
                              STATE_DOES_NOT_EXISTS)

from customer.models import City, Country, Customer, GenderType, State
from customer.serializers import (AddCitySerializer,
                                  AddCountrySerializer,
                                  AddStateSerializer,
                                  EditAddressInfoSerializer,
                                  EditPersonalInfoSerializer,
                                  FetchAddressInfoSerializer,
                                  FetchCitySerializer,
                                  FetchCountrySerializer,
                                  FetchPersonalInfoSerializer,
                                  FetchStateSerializer)

from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from security.customer_authorization import CustomerJWTAuthentication


class ProfilePersonalInfo(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            return GenericSuccessResponse(FetchPersonalInfoSerializer(customer).data, message=PERSONAL_INFO_UPDATED_SUCCESSFULLY, status=200)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)

    @staticmethod
    def patch(request):
        try:
            if ("first_name" not in request.data or request.data["first_name"] == "" or
                "middle_name" not in request.data or
                        "last_name" not in request.data or
                    "contact_number" not in request.data or
                    "gender" not in request.data or
                "age" not in request.data
                ):
                return CustomBadRequest(message=BAD_REQUEST)

            if request.data["gender"] not in GenderType.choices():
                return CustomBadRequest(message=DATA_IS_INVALID)

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            personal_info_serializer = EditPersonalInfoSerializer(
                customer, data=request.data)

            if personal_info_serializer.is_valid():
                personal_info_serializer.save()

                return GenericSuccessResponse(message=PERSONAL_INFO_UPDATED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)


class ProfileAddressInfo(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            return GenericSuccessResponse(FetchAddressInfoSerializer(customer).data, message=PERSONAL_INFO_UPDATED_SUCCESSFULLY, status=200)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)

    @staticmethod
    def patch(request):
        try:
            if ("country" not in request.data or
                "state" not in request.data or
                        "city" not in request.data or
                    "postal_code" not in request.data or
                    "street" not in request.data
                ):
                return CustomBadRequest(message=BAD_REQUEST)

            if not Country.objects.filter(country_id=request.data["country"]).exists():
                return CustomBadRequest(message=COUNTRY_DOES_NOT_EXISTS)

            if not State.objects.filter(state_id=request.data["state"]).exists():
                return CustomBadRequest(message=STATE_DOES_NOT_EXISTS)

            if not City.objects.filter(city_id=request.data["city"]).exists():
                return CustomBadRequest(message=CITY_DOES_NOT_EXISTS)

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            address_info_serializer = EditAddressInfoSerializer(
                customer, data=request.data)

            if address_info_serializer.is_valid():
                address_info_serializer.save()

                return GenericSuccessResponse(message=ADDRESS_INFO_UPDATED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)


class CountryManagement(APIView):
    @staticmethod
    def get(request):
        try:
            country = Country.objects.filter(is_deleted=False)

            return GenericSuccessResponse(FetchCountrySerializer(country, many=True).data, message="country fetched successfully", status=200)

        except:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if ("country_name" not in request.data or request.data["country_name"] == "" or
               "country_code" not in request.data or request.data["country_code"] == ""):
                return CustomBadRequest(message=BAD_REQUEST)

            if Country.objects.filter(country_name=request.data["country_name"]).exists():
                return CustomBadRequest(message="country already exists")

            if Country.objects.filter(country_code=request.data["country_code"]).exists():
                return CustomBadRequest(message="country code already exists")

            add_country_serializer = AddCountrySerializer(data=request.data)

            if add_country_serializer.is_valid():
                add_country_serializer.save()

                return GenericSuccessResponse(message="country added successfully", status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except:
            return GenericException()


class StateManagement(APIView):
    @staticmethod
    def get(request):
        try:
            state = State.objects.filter(is_deleted=False)

            return GenericSuccessResponse(FetchStateSerializer(state, many=True).data, message="state fetched successfully", status=200)

        except:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if "state_name" not in request.data or request.data["state_name"] == "" or "state_code" not in request.data or request.data["state_code"] == "" or "country" not in request.data or request.data["country"] == "":
                return CustomBadRequest(message=BAD_REQUEST)

            if not Country.objects.filter(country_id=request.data["country"]).exists():
                return CustomBadRequest(message="country does not exists")

            if State.objects.filter(state_name=request.data["state_name"]).exists():
                return CustomBadRequest(message="state already exists")

            if State.objects.filter(state_code=request.data["state_code"]).exists():
                return CustomBadRequest(message="state code already exists")

            add_state_serializer = AddStateSerializer(data=request.data)

            if add_state_serializer.is_valid():
                add_state_serializer.save()

                return GenericSuccessResponse(message="state added successfully", status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except:
            return GenericException()


class CityManagement(APIView):
    @staticmethod
    def get(request):
        try:
            city = City.objects.filter(is_deleted=False)

            return GenericSuccessResponse(FetchCitySerializer(city, many=True).data, message="city fetched successfully", status=200)

        except:
            return GenericException()

    @staticmethod
    def post(request):
        try:
            if "city_name" not in request.data or request.data["city_name"] == "" or "state" not in request.data or request.data["state"] == "":
                return CustomBadRequest(message=BAD_REQUEST)

            if not State.objects.filter(state_id=request.data["state"]).exists():
                return CustomBadRequest(message="state does not exists")

            if City.objects.filter(city_name=request.data["city_name"]).exists():
                return CustomBadRequest(message="city already exists")

            add_city_serializer = AddCitySerializer(data=request.data)

            if add_city_serializer.is_valid():
                add_city_serializer.save()

                return GenericSuccessResponse(message="city added successfully", status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except:
            return GenericException()
