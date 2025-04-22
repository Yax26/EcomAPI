from django.urls import path

from .views import HomePageMA, HomePageWA


app_name = "homepage"

urlpatterns = [

    path("homepagema/", HomePageMA.as_view()),

    path("homepagewa/", HomePageWA.as_view()),


]
