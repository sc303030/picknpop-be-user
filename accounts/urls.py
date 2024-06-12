from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"sign-up", SignUpViewSet, basename="sign-up")

urlpatterns = [
    path("sign-in/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
