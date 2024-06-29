import pytest


@pytest.fixture
def user():
    return {
        "email": "test@test.com",
        "username": "test@test.com",
        "password": "test",
        "first_name": "Test First Name",
        "last_name": "Test Last Name"
    }
