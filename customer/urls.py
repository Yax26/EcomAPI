from django.urls import path

from .profile import AddCity, AddState, CountryManagement, ProfileAddressInfo, ProfilePersonalInfo

from .views import Registration, Logout, Login, ResetPassword


app_name = "customer"

urlpatterns = [

    path("registration/", Registration.as_view()),

    path("logout/", Logout.as_view()),

    path("login/", Login.as_view()),

    path("resetpassword/", ResetPassword.as_view()),

    path("personalinfo/", ProfilePersonalInfo.as_view()),

    path("addressinfo/", ProfileAddressInfo.as_view()),

    path("country/", CountryManagement.as_view()),

    path("state/", AddState.as_view()),

    path("city/", AddCity.as_view())



]
