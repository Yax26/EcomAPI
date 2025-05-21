from django.urls import path

from .profile import FetchProfileInfo, ProfileAddressInfo, ProfilePersonalInfo

from .views import Registration, Logout, Login, ResetPassword


app_name = "customer"

urlpatterns = [

    path("registration/", Registration.as_view()),

    path("logout/", Logout.as_view()),

    path("login/", Login.as_view()),

    path("resetpassword/", ResetPassword.as_view()),

    path("profileinfo/", FetchProfileInfo.as_view()),

    path("personalinfo/", ProfilePersonalInfo.as_view()),

    path("addressinfo/", ProfileAddressInfo.as_view()),

    # path("country/", CountryManagement.as_view()),

    # path("state/", StateManagement.as_view()),

    # path("city/", CityManagement.as_view())



]
