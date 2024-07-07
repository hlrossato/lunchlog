from typing import Any, TYPE_CHECKING
from django.contrib.auth.models import BaseUserManager

if TYPE_CHECKING:
    from users.models import CustomUser


class UserCustomManager(BaseUserManager):
    """User custom manager - Making sure users can signup with their
    email addresses
    """

    def create(self, **kwargs: dict) -> Any:
        email = str(kwargs.pop("email", ""))
        password = str(kwargs.pop("password", ""))
        return self._create_user(email=email, password=password, **kwargs)

    def _create_user(
        self, email: str, password: str, **extra_fields: Any
    ) -> "CustomUser":
        if not email:
            raise ValueError("Users must enter their email address")

        if not password:
            raise ValueError("Users must enter their email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> Any:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)
