import pytest

from users.models import CustomUser


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(email="test@test.com", password="test")
    assert user is not None


@pytest.mark.django_db
def test_create_user__value_error():
    with pytest.raises(ValueError):
        CustomUser.objects.create_user(email=None, password="test")


@pytest.mark.django_db
def test_create_superuser():
    user = CustomUser.objects.create_superuser(email="test@test.com", password="test")
    assert user.is_superuser is True
    assert user.is_staff is True
