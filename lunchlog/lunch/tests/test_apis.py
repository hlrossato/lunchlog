import pytest
import uuid
from io import BytesIO
from unittest import mock
from decimal import Decimal
from datetime import datetime, timezone
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import encode_multipart
from django.urls import reverse_lazy
from rest_framework import status
from google_places_api.api import GooglePlaceDetail
from lunch.models import Receipt

receipt_api = reverse_lazy("lunch:receipt")


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_receipt_create_api__successful(
    mocked_place_id,
    mocked_place_details,
    receipt_input_data,
    auth_client,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    response = auth_client.post(receipt_api, data=receipt_input_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Receipt.objects.count() == 1


@pytest.mark.django_db
def test_receipt_create_api__unauthorized_user(receipt_input_data, client):
    response = client.post(receipt_api, data=receipt_input_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_receipt_create_api__bad_request(receipt_input_data, auth_client):
    receipt_input_data.pop("price")
    response = auth_client.post(receipt_api, data=receipt_input_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_receipt_list_api(
    mocked_place_id,
    mocked_place_details,
    receipt_data,
    auth_client,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    for _ in range(5):
        Receipt.objects.create(**receipt_data)

    response = auth_client.get(receipt_api)
    assert len(response.json()) == 5
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_receipt_list_api__filter_successful(
    mocked_place_id,
    mocked_place_details,
    receipt_data,
    auth_client,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    for _ in range(5):
        Receipt.objects.create(**receipt_data)

    for _ in range(2):
        receipt_data["date"] = datetime(
            day=12, month=3, year=2024, tzinfo=timezone.utc
        ).date()
        Receipt.objects.create(**receipt_data)

    for _ in range(3):
        receipt_data["date"] = datetime(
            day=12, month=5, year=2024, tzinfo=timezone.utc
        ).date()
        Receipt.objects.create(**receipt_data)

    assert Receipt.objects.count() == 10

    response = auth_client.get(f"{receipt_api}?month=3")
    assert len(response.json()) == 2
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_receipt_list_api__filter_unsuccessful(auth_client):
    response = auth_client.get(f"{receipt_api}?month=2")
    assert len(response.json()) == 0
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_receipt_update_api__successful(
    mocked_place_id,
    mocked_place_details,
    receipt_input_data,
    auth_client,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    response = auth_client.post(receipt_api, data=receipt_input_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert (
        response.json()["price"] == Decimal(receipt_input_data["price"]).to_eng_string()
    )

    new_price = Decimal("80.50").quantize(Decimal(".00"))
    data = {"price": new_price}
    receipt_update_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": response.json()["uuid"]}
    )

    response = auth_client.patch(
        receipt_update_api, data=data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["price"] == new_price.to_eng_string()


@pytest.mark.django_db
def test_receipt_update_api__successful__new_image(
    receipt,
    auth_client,
):
    assert receipt

    def new_image():
        image_data = BytesIO()
        image = Image.new("RGB", (10, 10), "black")
        image.save(image_data, format="png")
        image_data.seek(0)
        return SimpleUploadedFile(
            "another_image.png", image_data.read(), content_type="image/png"
        )

    receipt_update_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": str(receipt.uuid)}
    )

    image = new_image()
    data = {"image": image}

    content = encode_multipart("BoUnDaRyStRiNg", data)
    content_type = "multipart/form-data; boundary=BoUnDaRyStRiNg"
    response = auth_client.patch(receipt_update_api, content, content_type=content_type)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_receipt_update_api__unauthorized_client(receipt, client):
    assert receipt

    new_price = Decimal("80.50").quantize(Decimal(".00"))
    data = {"price": new_price}

    receipt_update_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": str(receipt.uuid)}
    )

    response = client.patch(
        receipt_update_api, data=data, content_type="application/json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_receipt_delete_api__successful(receipt, auth_client):
    assert receipt

    receipt_delete_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": str(receipt.uuid)}
    )
    response = auth_client.delete(receipt_delete_api)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_receipt_delete_api__unauthorized_user(receipt, auth_client, client):
    assert receipt

    receipt_delete_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": str(receipt.uuid)}
    )
    response = client.delete(receipt_delete_api)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_receipt_delete_api__receipt_not_found(receipt, auth_client):
    assert receipt

    receipt_delete_api = reverse_lazy(
        "lunch:receipt-detail", kwargs={"uuid": uuid.uuid4()}
    )
    response = auth_client.delete(receipt_delete_api)
    assert response.status_code == status.HTTP_404_NOT_FOUND
