# tests.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Post, Comment

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@test.com", password="testpassword")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_post(user):
    post_data = {"title": "Test Title", "content": "Test Content", "owner": user}
    post = Post.objects.create(**post_data)

    assert Post.objects.count() == 1
    assert Post.objects.first().title == "Test Title"
    assert Post.objects.first().content == "Test Content"
    assert Post.objects.first().owner == user


@pytest.mark.django_db
def test_add_comment_to_post(api_client, user):
    api_client.login(email="testuser@test.com", password="testpassword")

    post = Post.objects.create(title="Test Post", content="Test Content", owner=user)

    comment = Comment.objects.create(author=user, post=post, message="Test Comment")

    assert Comment.objects.count() == 1
    assert Comment.objects.get().message == "Test Comment"
    assert Comment.objects.get().post == post
    assert Comment.objects.get().author == user

    api_client.logout()
