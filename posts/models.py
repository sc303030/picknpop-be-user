from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def team_emblem_upload_to(instance, filename):
    return f"team_emblems/{instance.league}/{filename}"


class Team(BaseModel):
    class LeagueChoices(models.TextChoices):
        KBL = "KBL", "한국프로농구"

    name = models.CharField(max_length=255, unique=True)
    league = models.CharField(
        max_length=5, default=LeagueChoices.KBL, choices=LeagueChoices.choices
    )
    emblem = models.ImageField(upload_to=team_emblem_upload_to, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.league})"

    class Meta:
        ordering = ["-name"]


class Post(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="my_post_set", on_delete=models.CASCADE
    )
    team = models.ForeignKey(Team, related_name="team_posts", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ["-id"]
