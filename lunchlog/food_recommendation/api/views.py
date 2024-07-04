from rest_framework.generics import ListAPIView
from food_recommendation.api.serializers import FoodRecommendationModelSerializer


class FoodRecommendationListAPIView(ListAPIView):
    serializer_class = FoodRecommendationModelSerializer

    # def get_queryset(self):
    #     return Restaurant.objects
