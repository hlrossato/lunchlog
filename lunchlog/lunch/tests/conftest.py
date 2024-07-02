import pytest
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
def receipt(receipt_data):
    return Receipt.objects.create(**receipt_data)
