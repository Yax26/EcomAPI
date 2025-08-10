from decimal import Decimal
from rest_framework.views import APIView
from decimal import Decimal, ROUND_HALF_UP

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
    def post(request):
        try:
            print("testing1")

            if "product_id" not in request.data or request.data["product_id"] == "":
                return CustomBadRequest(message=BAD_REQUEST)

            customer_id = request.user.customer_id
            request.data["customer_id"] = customer_id

            product_details = Products.objects.get(
                product_id=request.data["product_id"], is_deleted=False)
            print("testing2")

            if Cart.objects.filter(is_deleted=False, is_checked_out=False, customer_id=customer_id).exists():

                cart = Cart.objects.filter(
                    is_deleted=False, is_checked_out=False, customer_id=customer_id).last()

                product_found = False
                print("testing3")

                for i in cart.products:
                    print("ids", i["product_id"], request.data["product_id"])
                    if i["product_id"] == request.data["product_id"]:
                        if "action" in request.data and request.data["action"] == "remove":
                            print("-----", i["product_quantity"])
                            if i["product_quantity"] > 1:
                                i["product_quantity"] -= 1
                            else:
                                print("before remove", cart.products)
                                cart.products.remove(i)
                                print("after remove", cart.products)
                        else:
                            i["product_quantity"] += 1
                            print("+++++", i["product_quantity"])

                        product_found = True
                print(product_found)
                if product_found == False:
                    products = {"product_id": product_details.product_id,
                                "product_price": str(product_details.product_price),
                                "product_image": str(product_details.product_image),
                                "product_name": product_details.product_name,
                                "product_quantity": 1}

                    cart.products.append(products)

                TWO_PLACES = Decimal('0.01')
                print(cart.products)
                if len(cart.products) > 0:
                    print(cart)
                    cart.sub_total = sum(
                        Decimal(p["product_price"]) * p["product_quantity"]
                        for p in cart.products
                    ).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                    cart.delivery_fees = (Decimal(
                        '5') * cart.sub_total / Decimal('100')).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                    cart.tax = (Decimal('13') * cart.sub_total / Decimal('100')
                                ).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                    cart.total = (cart.sub_total + cart.delivery_fees +
                                  cart.tax).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
                else:
                    cart.sub_total = 0

                    cart.delivery_fees = 0

                    cart.tax = 0

                    cart.total = 0

                print("cart", cart)

                cart.save()

                return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

            else:

                products = [{"product_id": product_details.product_id,
                             "product_price": str(product_details.product_price),
                             "product_image": str(product_details.product_image),
                             "product_name": product_details.product_name,
                             "product_quantity": 1}
                            ]
                request.data["products"] = products

                TWO_PLACES = Decimal("0.01")

                total_amount = Decimal(str(product_details.product_price)).quantize(
                    TWO_PLACES, rounding=ROUND_HALF_UP)

                request.data["sub_total"] = total_amount

                request.data["delivery_fees"] = (Decimal(
                    '5') * total_amount / Decimal('100')).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                request.data["tax"] = (Decimal(
                    '13') * total_amount / Decimal('100')).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                request.data["total"] = (request.data["sub_total"] + request.data["delivery_fees"] +
                                         request.data["tax"]).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

                cart_serializer = CartSerializer(data=request.data)

                if cart_serializer.is_valid(raise_exception=True):
                    cart_serializer.save()

                    return GenericSuccessResponse(data=FetchCartSerializer(cart).data, message=DATA_ADDED_TO_CART_SUCCESSFULLY, status=201)

                else:
                    return CustomBadRequest(DATA_IS_INVALID)

        except Products.DoesNotExist:
            return CustomBadRequest(message=DATA_NOT_FOUND)

        except Exception:
            return GenericException(request=request)
