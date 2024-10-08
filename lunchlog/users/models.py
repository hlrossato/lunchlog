from users.managers import UserCustomManager
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None

    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name="First name", max_length=30, blank=True)
    last_name = models.CharField(verbose_name="Last name", max_length=150, blank=True)
    email = models.EmailField(verbose_name="Email", unique=True, null=True)
    is_staff = models.BooleanField(
        verbose_name="Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    objects = UserCustomManager()
