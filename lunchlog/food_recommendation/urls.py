from django.urls import path
from food_recommendation.api import views

app_name = "food_recommendation"

urlpatterns = [
    path("", views.FoodRecommendationListAPIView.as_view(), name="food-recommendation"),
]
