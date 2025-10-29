from rest_framework.views import APIView

from cart.models import Cart
from cart.serializers import CartSerializer, FetchCartSerializer

from common.constants import (BAD_REQUEST,
                              DATA_ADDED_TO_CART_SUCCESSFULLY,
                              DATA_IS_INVALID,
                              FETCHED_CART_DATA_SUCCESSFULLY,
                              YOUR_CART_IS_EMPTY)

from exceptions.generic_response import GenericSuccessResponse
from exceptions.generic import CustomBadRequest, GenericException

from products.models import Products

from security.customer_authorization import CustomerJWTAuthentication


class CartManagement(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):
        try:
            if Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).exists():

                cart = Cart.objects.filter(
                    is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).last()

                return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=FETCHED_CART_DATA_SUCCESSFULLY, status=200)

            else:
                return CustomBadRequest(message=YOUR_CART_IS_EMPTY)

        except Exception:
            return GenericException(request=request)

    @staticmethod
    def patch(request):
        try:
            if request.data["cart"] == "" or "cart" not in request.data:
                return CustomBadRequest(message=BAD_REQUEST)

            cart = request.data['cart']

            cart["customer_id"] = request.user.customer_id

            if not Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).exists():
                cart_serializer = CartSerializer(data=request.data['cart'])

                if cart_serializer.is_valid(raise_exception=True):
                    cart_serializer.save()
                    return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=200)
                else:
                    return CustomBadRequest(DATA_IS_INVALID)

            cart = Cart.objects.filter(
                is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).last()

            cart_serializer = FetchCartSerializer(
                cart, data=request.data['cart'])

            if cart_serializer.is_valid(raise_exception=True):
                cart_serializer.save()
                return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=200)

            else:
                return CustomBadRequest(DATA_IS_INVALID)

        except Exception as e:
            return GenericException(request=request)
