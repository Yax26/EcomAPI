from django.urls import path

from .views import AddBannerData, AddFeatureData, HomePageMA, HomePageWA


app_name = "homepage"

urlpatterns = [

    path("mobile/", HomePageMA.as_view()),

    path("web/", HomePageWA.as_view()),

    path("addfeature/", AddFeatureData.as_view()),

    path("addbanner/", AddBannerData.as_view()),


]
