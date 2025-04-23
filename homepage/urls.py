from django.urls import path

from .views import HomePageMA, HomePageWA


app_name = "homepage"

urlpatterns = [

    path("mobile/", HomePageMA.as_view()),

    path("web/", HomePageWA.as_view()),


]
