import pytest
from users.api.serializers import SignUpModelSerializer


@pytest.mark.django_db
def test_user_signup_serializer(user_signup_data):
    serializer = SignUpModelSerializer(data=user_signup_data)
    assert serializer.is_valid()
    assert serializer.data == user_signup_data
