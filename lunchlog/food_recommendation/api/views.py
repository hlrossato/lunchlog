from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from food_recommendation.api.serializers import (
    FoodRecommendationModelSerializer,
)
from lunch.models import Restaurant


class FoodRecommendationSearchFilter(filters.SearchFilter):
    search_param = "city"

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        print(search_terms)

        if not search_terms:
            return queryset.none()

        return super().filter_queryset(request, queryset, view)


class FoodRecommendationListAPIView(ListAPIView):
    serializer_class = FoodRecommendationModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = [
        FoodRecommendationSearchFilter,
    ]
    search_fields = [
        "city",
    ]

    def get_queryset(self):
        queryset = Restaurant.objects.filter(user=self.request.user)
        return queryset
