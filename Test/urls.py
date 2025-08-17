from django.urls import path

from Test.views import TestAPI


app_name = "Test"

urlpatterns = [

    path("", TestAPI.as_view()),

]
