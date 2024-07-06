from rest_framework import serializers
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class SignUpModelSerializer(UserSerializer):
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ["password"]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
