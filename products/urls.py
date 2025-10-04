from django.urls import path

from .views import AddProductData, FeaturedProductsSortAndFilter, ProductRating, ProductsDetails, SortAndFilterProducts


app_name = "products"

urlpatterns = [

    # path("search/", SearchedProducts.as_view()),

    path("add/", AddProductData.as_view()),

    # path("features/", FeaturedProducts.as_view()),

    path("rating/", ProductRating.as_view()),

    path("details/", ProductsDetails.as_view()),

    path("sortandfilter/", SortAndFilterProducts.as_view()),

    path("featuredsorting/", FeaturedProductsSortAndFilter.as_view()),

]
