import pytest
from unittest import mock
from lunch.models import Receipt
from google_places_api.api import GooglePlaceDetail


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_receipt__created(
    mocked_place_id,
    mocked_place_details,
    receipt_data,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    receipt = Receipt.objects.create(**receipt_data)
    assert receipt is not None
