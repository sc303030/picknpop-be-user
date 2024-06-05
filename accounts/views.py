from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import SignUpSerializer
from .models import User


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
