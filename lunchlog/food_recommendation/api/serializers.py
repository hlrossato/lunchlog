from rest_framework import serializers
from lunch.models import Restaurant


class FoodRecommendationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
