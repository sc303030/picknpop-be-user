from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserDeleteView

router = DefaultRouter()

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("allauth/", include("allauth.urls")),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
]
