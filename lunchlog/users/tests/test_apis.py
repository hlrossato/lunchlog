import pytest
from django.urls import reverse_lazy
from users.models import CustomUser
from users.api.serializers import SignUpModelSerializer

user_sign_up_url = reverse_lazy("users:user-signup")
user_sign_in_url = reverse_lazy("users:user-signin")


@pytest.mark.django_db
def test_user_signup(user_signup_data, client, user_detail_data):
    response = client.post(user_sign_up_url, user_signup_data)
    assert response.status_code == 201
    assert response.json() == user_detail_data
    assert CustomUser.objects.last() is not None


@pytest.mark.django_db
def test_user_signin(user, user_detail_data, client):
    login_data = {
        "email": user.email,
        "password": "test"
    }
    response = client.post(user_sign_in_url, login_data)
    assert response.status_code == 202
    assert response.json() == user_detail_data


@pytest.mark.django_db
def test_user_signin__bad_request(user, client):
    login_data = {
        "password": "test"
    }
    response = client.post(user_sign_in_url, login_data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_signin__user_not_found(user, client):
    login_data = {
        "email": "hello",
        "password": "test"
    }
    response = client.post(user_sign_in_url, login_data)
    assert response.status_code == 404
