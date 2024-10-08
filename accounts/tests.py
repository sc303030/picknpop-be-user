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
        "nickname": "testnickname",
        "password": "testpassword",
        "username": "test@example.com",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == "test@example.com"


@pytest.mark.django_db
def test_login_user(api_client):
    User.objects.create_user(
        nickname="testnickname", password="testpassword", username="test@example.com"
    )
    url = reverse("token_obtain_pair")
    data = {"username": "test@example.com", "password": "testpassword"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_token(api_client):
    User.objects.create_user(
        nickname="testnickname",
        password="testpassword",
        username="test@example.com",
    )
    login_url = reverse("token_obtain_pair")
    login_data = {"username": "test@example.com", "password": "testpassword"}
    login_response = api_client.post(login_url, login_data, format="json")

    refresh_url = reverse("token_refresh")
    refresh_data = {"refresh": login_response.data["refresh"]}
    refresh_response = api_client.post(refresh_url, refresh_data, format="json")

    assert refresh_response.status_code == status.HTTP_200_OK
    assert "access" in refresh_response.data


@pytest.mark.django_db
def test_register_user_with_existing_nickname(api_client):
    User.objects.create_user(
        nickname="testnickname",
        password="password",
        username="existing@example.com",
    )
    url = reverse("sign-up-list")
    data = {
        "nickname": "testnickname",
        "password": "newpassword",
        "username": "new@example.com",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nickname" in response.data
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_user_with_missing_fields(api_client):
    url = reverse("sign-up-list")
    data = {
        "nickname": "",
        "password": "",
        "username": "",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_registration_with_default_avatar(api_client):
    url = reverse("sign-up-list")
    data = {
        "username": "testuser",
        "password": "testpassword123",
        "nickname": "testnickname",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

    user = User.objects.get(username="testuser")
    assert user.nickname == "testnickname"
    assert user.avatar.name == ""
