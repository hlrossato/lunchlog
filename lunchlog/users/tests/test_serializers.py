import pytest
from users.api.serializers import UserModelSerializer


@pytest.mark.django_db
def test_user_signup_serializer(user):
    serializer = UserModelSerializer(data=user)
    assert serializer.is_valid() == True
    assert serializer.data == user
