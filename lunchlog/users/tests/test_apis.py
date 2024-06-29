import pytest
from django.urls import reverse_lazy
from users.models import User
from users.api.serializers import UserModelSerializer

user_sign_up_url = reverse_lazy("users:user-signup")


@pytest.mark.django_db
def test_user_signup(user, client):
    response = client.post(user_sign_up_url, user)
    assert response.status_code == 201
    assert response.json() == user
    assert User.objects.last() is not None
