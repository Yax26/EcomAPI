from django.urls import path

from .views import AddProductData, SearchedProducts


app_name = "homepage"

urlpatterns = [

    path("search/", SearchedProducts.as_view()),

    path("add/", AddProductData.as_view()),


]
