from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from food_recommendation.api.serializers import FoodRecommendationModelSerializer
from lunch.models import Restaurant


class FoodRecommendationListAPIView(ListAPIView):
    serializer_class = FoodRecommendationModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        city = self.request.query_params.get("city")
        if city:
            return Restaurant.objects.filter(city=city)
        return Restaurant.objects.all()
