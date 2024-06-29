from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from users.api.serializers import UserModelSerializer
from users.models import User


class UserSignUpView(CreateAPIView):
    model = User.objects.all()
    serializer_class = UserModelSerializer
