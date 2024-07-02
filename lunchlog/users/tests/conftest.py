import pytest


@pytest.fixture
def user_detail_data():
    return {
        "email": "test@test.com",
        "first_name": "Test First Name",
        "last_name": "Test Last Name",
    }
