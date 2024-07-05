import pytest
from django.urls import reverse_lazy
from rest_framework import status
from google_places_api.api import GooglePlaceDetail
from lunch.models import Restaurant

food_recommendation_api = reverse_lazy("food_recommendation:food-recommendation")


@pytest.mark.django_db
def test_food_recommendation__no_filter_empty_response(
    auth_client,
    google_place_detail,
    user,
):
    place = GooglePlaceDetail(google_place_detail["result"]).to_dict()

    for _ in range(5):
        Restaurant.objects.create(**place, user=user)

    assert Restaurant.objects.count() == 5

    response = auth_client.get(food_recommendation_api)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.django_db
def test_food_recommendation__successful(auth_client, google_place_detail, user):
    place = GooglePlaceDetail(google_place_detail["result"]).to_dict()

    for _ in range(5):
        Restaurant.objects.create(**place, user=user)

    google_place_detail["result"]["address_components"][3]["long_name"] = "Dusseldorf"
    new_place = GooglePlaceDetail(google_place_detail["result"]).to_dict()

    for _ in range(2):
        Restaurant.objects.create(**new_place, user=user)

    assert Restaurant.objects.count() == 7

    response = auth_client.get(f"{food_recommendation_api}?city=Dusseldorf")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


def test_food_recommendation__unsuccessful(client):
    response = client.get(food_recommendation_api)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
