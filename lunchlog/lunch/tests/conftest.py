import pytest
from unittest import mock
from io import BytesIO
from PIL import Image
from datetime import datetime, timezone
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from lunch.models import Receipt

now = datetime.now(timezone.utc).date()


@pytest.fixture
def image():
    image_data = BytesIO()
    image = Image.new("RGB", (100, 100), "white")
    image.save(image_data, format="png")
    image_data.seek(0)
    return SimpleUploadedFile("test.png", image_data.read(), content_type="image/png")


@pytest.fixture
def receipt_data(image, user):
    return {
        "date": now,
        "price": "32.49",
        "restaurant_name": "Best Restaurant In Town",
        "user": user,
        "image": image,
        "restaurant_address": "Flower Str. 30, Dusseldorf, 40123",
    }


@pytest.fixture
def receipt_input_data(image, receipt_data):
    return {
        "date": now.isoformat(),
        "price": Decimal("32.49").quantize(Decimal(".00")),
        "restaurant_name": receipt_data["restaurant_name"],
        "restaurant_address": receipt_data["restaurant_address"],
        "image": image,
    }


@pytest.fixture
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def receipt(mocked_place_id, mocked_place_details, receipt_data, google_place_detail):
    from google_places_api.api import GooglePlaceDetail

    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    return Receipt.objects.create(**receipt_data)
