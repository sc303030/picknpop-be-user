from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(max_length=20, write_only=True, required=True)
    username = serializers.EmailField(required=True)
    email = serializers.EmailField(read_only=True)

    def validate_nickname(self, nickname):
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError(_("이미 존재 하는 닉네임 입니다."))
        return nickname

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["email"] = self.validated_data.get("username")
        return data

    def custom_signup(self, request, user):
        nickname = self.validated_data.pop("nickname")
        if nickname:
            user.nickname = nickname
            user.save()
