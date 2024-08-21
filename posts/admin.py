from django.contrib import admin

from posts.models import Post, Team, Emotion


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "league", "emblem")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content")


@admin.register(Emotion)
class PostAdmin(admin.ModelAdmin):
    pass
