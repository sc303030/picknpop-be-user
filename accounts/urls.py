from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignUpViewSet

router = DefaultRouter()
router.register(r"sign-up", SignUpViewSet, basename="sign-up")

urlpatterns = [
    path("", include(router.urls)),
]
