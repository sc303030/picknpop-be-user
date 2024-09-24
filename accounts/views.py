from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from dj_rest_auth.views import LoginView
from django.contrib.auth.models import User


User = get_user_model()


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(
            {"detail": "User account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"username": "해당 아이디를 찾을 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"password": "비밀번호가 틀렸습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = super().post(request, *args, **kwargs)
        return response
