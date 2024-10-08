from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import User


User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(
        max_length=20,
        write_only=True,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[가-힣a-zA-Z0-9]+$",
                message="문자와 숫자만 가능합니다.",
            )
        ],
    )
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


class CustomUserDetailsSerializer(UserDetailsSerializer):
    nickname = serializers.CharField(
        max_length=20,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[가-힣a-zA-Z0-9]+$",
                message="문자와 숫자만 가능합니다.",
            )
        ],
    )

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ("username", "nickname")

    def update(self, instance, validated_data):
        new_nickname = validated_data.get("nickname", instance.nickname)
        if User.objects.filter(nickname=new_nickname).exclude(id=instance.id).exists():
            raise serializers.ValidationError(
                {"nickname": "이미 존재하는 닉네임입니다."}
            )

        instance.nickname = new_nickname
        instance.save()
        return instance
