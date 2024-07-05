from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from lunch.models import Restaurant


class FoodRecommendationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class FoodRecommendationFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["city"]

    def validate_city(self, value):
        if not value:
            raise ValidationError("City must be provided")
        return value
