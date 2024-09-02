from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import SignUpSerializer, ProfileSerializer

User = get_user_model()


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = response.data["refresh"]
            access = response.data["access"]
            response.data["refresh_token"] = refresh
            response.data["access_token"] = access
        return response


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        if user_id is not None:
            queryset = User.objects.filter(id=user_id)
            if not queryset.exists():
                raise NotFound(f"User with id {user_id} not found.")
            return queryset
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
