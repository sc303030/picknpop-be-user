from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


class User(AbstractUser):
    avatar = ProcessedImageField(
        blank=True,
        null=True,
        upload_to="accounts/avatar/%Y/%m/%d",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 70},
    )
    nickname = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nickname}"
