from django.urls import path
from users.api import views

app_name = "users"

urlpatterns = [
    path("signup", views.UserSignUpView.as_view(), name="user-signup"),
    path("signin", views.UserSignInView.as_view(), name="user-signin"),
]
