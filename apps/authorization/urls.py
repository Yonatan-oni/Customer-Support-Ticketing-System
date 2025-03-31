from django.urls import path
from .views import sign_up, sign_in, signout, user_profile

urlpatterns = [
    path("signup/", sign_up, name="signup"),
    path("signin/", sign_in, name="signin"),
    path("signout/", signout, name="signout"),
    path("profile/", user_profile, name="profile"),
]
