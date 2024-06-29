from django.urls import path
from users.api import views as user_api_views

app_name = "users"

urlpatterns = [
    path("signup", user_api_views.UserSignUpView.as_view(), name="user-signup"),
]
