from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup/verify/", verifySignup, name="verify-signup"),
    path("login/", login, name="login"),
    path("delete/", deleteAccount, name="delete"),
    path("delete/verify/", verifyDelete, name="delete"),
]
