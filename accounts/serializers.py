from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "nickname",
            "password",
            "email",
        )

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError(_("이미 존재 하는 닉네임 입니다."))
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("이미 존재 하는 이메일 입니다."))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            nickname=validated_data["nickname"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user
