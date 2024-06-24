# tests.py

import pytest
from django.contrib.auth import get_user_model

from .models import Post

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(email="testuser@test.com", password="testpassword")


@pytest.mark.django_db
def test_create_post(user):
    post_data = {"title": "Test Title", "content": "Test Content", "owner": user}
    post = Post.objects.create(**post_data)

    assert Post.objects.count() == 1
    assert Post.objects.first().title == "Test Title"
    assert Post.objects.first().content == "Test Content"
    assert Post.objects.first().owner == user
