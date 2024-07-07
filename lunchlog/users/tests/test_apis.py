import pytest
from rest_framework import status
from django.urls import reverse_lazy
from users.models import CustomUser

user_sign_up_url = reverse_lazy("users:signup")
user_login_url = reverse_lazy("users:login")
user_logout_url = reverse_lazy("users:logout")


@pytest.mark.django_db
def test_user_signup(user_signup_data, client, user_detail_data):
    response = client.post(user_sign_up_url, user_signup_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == user_detail_data
    assert CustomUser.objects.last() is not None


@pytest.mark.django_db
def test_user_signin(user, user_detail_data, client):
    login_data = {"email": user.email, "password": "test"}
    response = client.post(user_login_url, login_data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == user_detail_data


@pytest.mark.django_db
def test_user_signin__bad_request(client):
    login_data = {"test": "test"}
    response = client.post(user_login_url, login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_signin__user_not_found(client):
    login_data = {"email": "hello", "password": "test"}
    response = client.post(user_login_url, login_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_logout(user, client, auth_client):
    login_data = {"email": user.email, "password": "test"}
    client.post(user_login_url, login_data)
    response = auth_client.get(user_logout_url)
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == user_login_url
