from django.urls import path
from users.api import views

app_name = "users"

urlpatterns = [
    path("signup", views.UserSignUpView.as_view(), name="user-signup"),
    path("login", views.UserLoginAPIView.as_view(), name="user-login"),
]
