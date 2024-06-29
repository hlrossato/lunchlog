from django.db import models
from django.contrib.auth.models import User as DjangoUser


class User(DjangoUser):
    USERNAME_FIELD = "email"


