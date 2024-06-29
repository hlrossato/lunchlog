import pytest
from users.models import CustomUser


@pytest.fixture
def user_signup_data():
    return {
        "email": "test@test.com",
        "password": "test",
        "first_name": "Test First Name",
        "last_name": "Test Last Name"
    }


@pytest.fixture
def user_detail_data():
    return {
        "email": "test@test.com",
        "first_name": "Test First Name",
        "last_name": "Test Last Name",
    }


@pytest.fixture
def user(user_signup_data):
    return CustomUser.objects.create_user(**user_signup_data)
