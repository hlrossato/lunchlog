from django.urls import path, include
from users import views
from users.api import views as api_views

app_name = "users"

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path("signup", api_views.UserSignUpView.as_view(), name="signup"),
                path("login", api_views.UserLoginAPIView.as_view(), name="login"),
                path("logout", api_views.UserLogoutAPIView.as_view(), name="logout"),
            ]
        ),
    ),
    path("", views.HomeView.as_view(), name="home"),
]
