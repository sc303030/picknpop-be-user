# tests.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Post, Comment, Team, EmotionType, Emotion

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser@test.com", email="testuser@test.com", password="testpassword"
    )


@pytest.fixture
def team():
    return Team.objects.create(
        name="서울 삼성",
        league=Team.LeagueChoices.KBL,
        emblem=None,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def emotion_type_like():
    return EmotionType.objects.create(name="Like")


@pytest.mark.django_db
def test_create_post(user, team):
    post_data = {
        "title": "Test Title",
        "content": "Test Content",
        "author": user,
        "team": team,
    }
    post = Post.objects.create(**post_data)

    assert Post.objects.count() == 1
    assert Post.objects.first().title == "Test Title"
    assert Post.objects.first().content == "Test Content"
    assert Post.objects.first().author == user


@pytest.mark.django_db
def test_add_comment_to_post(api_client, user, team):
    api_client.login(username="testuser@test.com", password="testpassword")

    post = Post.objects.create(
        title="Test Post", content="Test Content", author=user, team=team
    )
    comment = Comment.objects.create(author=user, post=post, message="Test Comment")

    assert Comment.objects.count() == 1
    assert Comment.objects.get().message == "Test Comment"
    assert Comment.objects.get().post == post
    assert Comment.objects.get().author == user

    api_client.logout()


@pytest.mark.django_db
def test_add_emotion_to_post(user, team, emotion_type_like):
    post = Post.objects.create(
        title="Test Post with Emotion", content="Test Content", author=user, team=team
    )
    emotion = Emotion.objects.create(
        user=user, post=post, emotion_type=emotion_type_like
    )

    assert Emotion.objects.count() == 1
    assert Emotion.objects.get().post == post
    assert Emotion.objects.get().user == user
    assert Emotion.objects.get().emotion_type == emotion_type_like
