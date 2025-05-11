from decimal import Decimal
import json
from rest_framework.views import APIView


from cart.models import Cart
from cart.serializers import CartSerializer

from common.constants import BAD_REQUEST, DATA_ADDED_TO_CART_SUCCESSFULLY, DATA_IS_INVALID, FETCHED_CART_DATA_SUCCESSFULLY, YOUR_CART_IS_EMPTY

from exceptions.generic_response import GenericSuccessResponse
from exceptions.generic import CustomBadRequest, GenericException

from products.models import Products

from security.customer_authorization import CustomerJWTAuthentication


class CartManagement(APIView):
    authentication_classes = [CustomerJWTAuthentication]

    @staticmethod
    def get(request):

        if Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).exists():

            cart = Cart.objects.filter(
                is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).last()

            return GenericSuccessResponse(data=CartSerializer(cart).data, message=FETCHED_CART_DATA_SUCCESSFULLY, status=200)
        else:
            return CustomBadRequest(message=YOUR_CART_IS_EMPTY)

    @staticmethod
    def post(request):
        try:
            if "product_id" not in request.data or request.data["product_id"] == "":
                return CustomBadRequest(message=BAD_REQUEST)

            customer_id = request.user.customer_id
            request.data["customer_id"] = customer_id

            product_details = Products.objects.get(
                product_id=request.data["product_id"], is_deleted=False)

            if Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=customer_id).exists():

                cart = Cart.objects.filter(
                    is_deleted=False, is_checked_out=False, customer_id=customer_id).last()

                cart.products[str(request.data["product_id"])] = str(
                    product_details.product_price)

                cart.total_amount = cart.total_amount + \
                    Decimal(str(product_details.product_price))

                cart.save()

                return GenericSuccessResponse(message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

            else:
                products = {str(request.data["product_id"]):
                            str(product_details.product_price)}
                request.data["products"] = products

                total_amount = Decimal(str(product_details.product_price))
                request.data["total_amount"] = total_amount

                cart_serializer = CartSerializer(data=request.data)

                if cart_serializer.is_valid(raise_exception=True):
                    cart_serializer.save()

                    return GenericSuccessResponse(message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

                else:
                    return CustomBadRequest(DATA_IS_INVALID)

        except Exception:
            return GenericException(request=request)
