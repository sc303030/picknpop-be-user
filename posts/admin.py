from django.contrib import admin

from posts.models import Post, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "league", "emblem")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content")
