from rest_framework.views import APIView
import phonenumbers
from phonenumbers import NumberParseException


from common.constants import (ADDRESS_INFO_UPDATED_SUCCESSFULLY,
                              BAD_REQUEST,
                              DATA_IS_INVALID,
                              DATA_NOT_FOUND, INVALID_PHONE_NUMBER, PERSONAL_INFO_FETCHED_SUCCESSFULLY,
                              PERSONAL_INFO_UPDATED_SUCCESSFULLY)

from customer.models import Customer
from customer.serializers import (
    EditAddressInfoSerializer, EditDepartmentSerializer,
    EditPersonalInfoSerializer,
    FetchProfileInfoSerializer)

from exceptions.generic import CustomBadRequest, GenericException
from exceptions.generic_response import GenericSuccessResponse

from security.customer_authorization import CustomerJWTAuthentication


class FetchProfileInfo(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            return GenericSuccessResponse(FetchProfileInfoSerializer(customer).data, message=PERSONAL_INFO_FETCHED_SUCCESSFULLY, status=200)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)

    @staticmethod
    def patch(request):
        try:
            if ("department" not in request.data):
                return CustomBadRequest(message=BAD_REQUEST)

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            edit_department_serializer = EditDepartmentSerializer(
                customer, data=request.data)

            if edit_department_serializer.is_valid(raise_exception=True):
                edit_department_serializer.save()

                return GenericSuccessResponse(message=PERSONAL_INFO_UPDATED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)


class ProfilePersonalInfo(APIView):
    authentication_classes = [CustomerJWTAuthentication]

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

            if request.data["gender"] not in ["MALE", "FEMALE", "OTHERS", "PREFER_NOT_TO_SAY"]:
                return CustomBadRequest(message="DATA_IS_INVALID")

            contact_number = request.data["contact_number"]
            parsed_number = phonenumbers.parse(contact_number)

            if not phonenumbers.is_valid_number(parsed_number):
                return CustomBadRequest(message=INVALID_PHONE_NUMBER)

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            personal_info_serializer = EditPersonalInfoSerializer(
                customer, data=request.data)

            if personal_info_serializer.is_valid(raise_exception=True):
                personal_info_serializer.save()

                return GenericSuccessResponse(message=PERSONAL_INFO_UPDATED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except NumberParseException:
            return CustomBadRequest(message=INVALID_PHONE_NUMBER_FORMAT)

        except Exception:
            return GenericException(request=request)


class ProfileAddressInfo(APIView):
    authentication_classes = [CustomerJWTAuthentication]

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

            customer = Customer.objects.get(
                customer_id=request.user.customer_id)

            address_info_serializer = EditAddressInfoSerializer(
                customer, data=request.data)

            if address_info_serializer.is_valid(raise_exception=True):
                address_info_serializer.save()

                return GenericSuccessResponse(message=ADDRESS_INFO_UPDATED_SUCCESSFULLY, status=200)

            return CustomBadRequest(message=DATA_IS_INVALID)

        except Customer.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)
