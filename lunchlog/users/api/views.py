from typing import TYPE_CHECKING, Self
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import (
    LoginSerializer,
    SignUpModelSerializer,
    UserSerializer,
)
from users.models import CustomUser

if TYPE_CHECKING:
    from requests import Request  # pragma: no cover


class UserSignUpView(CreateAPIView):
    model = CustomUser.objects.all()
    serializer_class = SignUpModelSerializer
    response_serializer_class = UserSerializer

    def create(
        self: Self, request: "Request", *args: tuple, **kwargs: dict
    ) -> "Response":
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.response_serializer_class(serializer.data).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(APIView):
    response_serializer_class = UserSerializer
    serializer_class = LoginSerializer

    def post(
        self: Self, request: "Request", *args: tuple, **kwargs: dict
    ) -> "Response":
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(username=email, password=password)
            if user and user.is_active:
                login(request, user)
                data = self.response_serializer_class(instance=user).data
                return Response(data, status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserLogoutAPIView(APIView):
    def get(
        self: Self, request: "Request", *args: tuple, **kwargs: dict
    ) -> HttpResponseRedirect:
        logout(request)
        return HttpResponseRedirect(reverse("users:login"))
