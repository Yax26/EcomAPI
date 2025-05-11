from django.urls import path

from .views import CartManagement


app_name = "cart"

urlpatterns = [

    path("management/", CartManagement.as_view()),

]
