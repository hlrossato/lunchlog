from rest_framework import serializers
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", "email", "password", "first_name", "last_name"
        ]
