import pytest
from datetime import datetime, timezone
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def image():
    return SimpleUploadedFile(
        name="foo.gif",
        content=b"""
            GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,
            \x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00
        """,
    )


@pytest.fixture
def receipt_data(image, user):
    now = datetime.now(timezone.utc)
    return {
        "date": now,
        "price": Decimal(32.49),
        "restaurant_name": "Best Restaurant In Town",
        "user": user,
        "file": image,
        "address": "Flower Str. 30, Dusseldorf, 40123",
    }
