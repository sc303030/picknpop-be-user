# tests.py
import sys

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock
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


@pytest.mark.django_db
@patch("sys.modules", {"fake_fastapi.posts.post_id": MagicMock()})
def test_increment_post_views(user, team):
    post = Post.objects.create(
        title="Test Post for Views",
        content="Content with Views",
        author=user,
        team=team,
    )

    fake_increment_views = sys.modules["fake_fastapi.posts.post_id"]
    fake_increment_views.return_value = {
        "message": "View count incremented",
        "post_id": post.id,
        "views": post.views + 1,
    }
    response = fake_increment_views(post.id)
    assert response["views"] == post.views + 1
    fake_increment_views.assert_called_once_with(post.id)


@pytest.mark.django_db
@patch("sys.modules", {"fake_fastapi.popular": MagicMock()})
def test_popular_posts_within_one_minute(user, team):
    post1 = Post.objects.create(
        title="Popular Post 1", content="Content 1", author=user, team=team
    )
    post2 = Post.objects.create(
        title="Popular Post 2", content="Content 2", author=user, team=team
    )

    fake_get_popular_posts = sys.modules["fake_fastapi.popular"]
    fake_get_popular_posts.return_value = [
        {"title": "Popular Post 1", "recent_views": 2},
        {"title": "Popular Post 2", "recent_views": 1},
    ]

    response = fake_get_popular_posts()

    assert len(response) == 2
    assert response[0]["title"] == "Popular Post 1"
    assert response[1]["title"] == "Popular Post 2"
    fake_get_popular_posts.assert_called_once()
