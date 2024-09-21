from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from accounts.views import ConfirmEmailView, success

router = DefaultRouter()

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("allauth/", include("allauth.urls")),
    re_path(
        r"^account-confirm-email/$",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("success/", success, name="success"),
]
