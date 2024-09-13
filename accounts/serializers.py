from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "nickname", "password", "avatar")

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError(_("이미 존재 하는 닉네임 입니다."))
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_("이미 존재 하는 ID 입니다."))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            nickname=validated_data["nickname"],
            password=validated_data["password"],
            username=validated_data["username"],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    old_password = serializers.CharField(required=False, write_only=True)
    new_password = serializers.CharField(required=False, write_only=True)
    new_password_confirm = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "nickname",
            "avatar",
            "old_password",
            "new_password",
            "new_password_confirm",
        )
        extra_kwargs = {
            "username": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if old_password or new_password or new_password_confirm:
            if not user.check_password(old_password):
                raise serializers.ValidationError(
                    {"old_password": _("현재 비밀번호가 일치하지 않습니다.")}
                )

            if new_password != new_password_confirm:
                raise serializers.ValidationError(
                    {"new_password_confirm": _("새로운 비밀번호가 일치하지 않습니다.")}
                )

        return attrs

    def update(self, instance, validated_data):
        if "nickname" in validated_data:
            instance.nickname = validated_data["nickname"]

        if "avatar" in validated_data:
            instance.avatar = validated_data["avatar"]

        if "new_password" in validated_data:
            instance.set_password(validated_data["new_password"])

        instance.save()
        return instance
