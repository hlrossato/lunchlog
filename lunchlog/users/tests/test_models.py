from django.test import TestCase
from users.models import User


class TestUserModel(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="test@test.com",
            email="test@test.com",
            password="test"
        )
        self.assertTrue(user)
