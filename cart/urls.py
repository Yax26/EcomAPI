from django.urls import path

from .views import AddToCart, CartManagement


app_name = "cart"

urlpatterns = [

    path("management/", CartManagement.as_view()),
    # path("addtocart/", AddToCart.as_view()),

]
