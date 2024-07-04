from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import (
    SignInSerializer,
    SignUpModelSerializer,
    UserSerializer,
)
from users.models import CustomUser


class UserSignUpView(CreateAPIView):
    model = CustomUser.objects.all()
    serializer_class = SignUpModelSerializer
    response_serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.response_serializer_class(serializer.data).data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserSignInView(APIView):
    response_serializer_class = UserSerializer
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                data = self.response_serializer_class(instance=user).data
                return Response(data, status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)
