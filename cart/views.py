from decimal import Decimal
from rest_framework.views import APIView


from cart.models import Cart
from cart.serializers import CartSerializer, FetchCartSerializer

from common.constants import (BAD_REQUEST,
                              DATA_ADDED_TO_CART_SUCCESSFULLY,
                              DATA_IS_INVALID, DATA_NOT_FOUND,
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

        if Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).exists():

            cart = Cart.objects.filter(
                is_deleted=False, is_checked_out=False, customer_id=request.user.customer_id).last()

            return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=FETCHED_CART_DATA_SUCCESSFULLY, status=200)

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

                product_found = False
                for i in cart.products:
                    if i["product_id"] == request.data["product_id"]:
                        i["product_quantity"] += 1
                        product_found = True

                if product_found == False:
                    products = {"product_id": product_details.product_id,
                                "product_price": str(product_details.product_price),
                                "product_image": str(product_details.product_image),
                                "product_name": product_details.product_name,
                                "product_quantity": 1}

                    cart.products.append(products)

                cart.sub_total += Decimal(
                    str(product_details.product_price))

                cart.delivery_fees = 5 * cart.sub_total / 100

                cart.tax = 13 * cart.sub_total / 100

                cart.total = cart.sub_total + cart.delivery_fees + cart.tax

                cart.save()

                return GenericSuccessResponse(message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

            else:

                products = [{"product_id": product_details.product_id,
                             "product_price": str(product_details.product_price),
                             "product_image": str(product_details.product_image),
                             "product_name": product_details.product_name,
                             "product_quantity": 1}
                            ]
                request.data["products"] = products

                total_amount = Decimal(str(product_details.product_price))

                request.data["sub_total"] = total_amount
                request.data["delivery_fees"] = 5 * total_amount / 100
                request.data["tax"] = 13 * total_amount / 100
                request.data["total"] = total_amount + \
                    request.data["delivery_fees"] + request.data["tax"]

                cart_serializer = CartSerializer(data=request.data)

                if cart_serializer.is_valid(raise_exception=True):
                    cart_serializer.save()

                    return GenericSuccessResponse(message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

                else:
                    return CustomBadRequest(DATA_IS_INVALID)

        except Products.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)
