import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse("sign-up-list")
    data = {
        "username": "testuser",
        "nickname": "testnickname",
        "password": "testpassword",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == "testuser"


@pytest.mark.django_db
def test_login_user(api_client):
    User.objects.create_user(
        username="testuser",
        nickname="testnickname",
        password="testpassword",
        email="test@example.com",
    )
    url = reverse("token_obtain_pair")
    data = {"username": "testuser", "password": "testpassword"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_token(api_client):
    User.objects.create_user(
        username="testuser",
        nickname="testnickname",
        password="testpassword",
        email="test@example.com",
    )
    login_url = reverse("token_obtain_pair")
    login_data = {"username": "testuser", "password": "testpassword"}
    login_response = api_client.post(login_url, login_data, format="json")

    refresh_url = reverse("token_refresh")
    refresh_data = {"refresh": login_response.data["refresh"]}
    refresh_response = api_client.post(refresh_url, refresh_data, format="json")

    assert refresh_response.status_code == status.HTTP_200_OK
    assert "access" in refresh_response.data


@pytest.mark.django_db
def test_register_user_with_existing_nickname(api_client):
    User.objects.create_user(
        username="existinguser",
        nickname="testnickname",
        password="password",
        email="existing@example.com",
    )
    url = reverse("sign-up-list")
    data = {
        "username": "newuser",
        "nickname": "testnickname",
        "password": "newpassword",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nickname" in response.data
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_user_with_missing_fields(api_client):
    url = reverse("sign-up-list")
    data = {
        "username": "",
        "nickname": "",
        "password": "",
        "email": "",
        "first_name": "",
        "last_name": "",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
