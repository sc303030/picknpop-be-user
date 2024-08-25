from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import resolve_url


class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)
    avatar = models.ImageField(
        blank=True,
        upload_to="accounts/avatar/%Y/%m/%d",
        help_text="48px * 48px 크기의 png/jpg 파일을 업로드해주세요.",
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return None

    def __str__(self):
        return f"{self.nickname}"
