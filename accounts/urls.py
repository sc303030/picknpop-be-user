from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet, MyTokenObtainPairView, ProfileViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r"sign-up", SignUpViewSet, basename="sign-up")
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("sign-in/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
