import pytest
from unittest import mock
from django.test import override_settings
from lunch.models import Restaurant
from lunch.services import populate_restaurant
from google_places_api.api import GooglePlaceDetail


@pytest.mark.django_db
@override_settings(USE_GOOGLE_PLACES=True)
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_populate_restaurant(
    mocked_place_id, mocked_place_details, receipt, google_place_detail
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    populate_restaurant(receipt)
    restaurant = Restaurant.objects.last()
    assert restaurant is not None
