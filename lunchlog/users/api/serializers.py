from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class SignUpModelSerializer(UserSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ["password"]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate_email(self, value):
        if not value:
            raise ValidationError("Email must be provided")
        return value

    def validate_password(self, value):
        if not value:
            raise ValidationError("Password must be provided")
        return value
