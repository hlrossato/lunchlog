import pytest
from unittest import mock
from django.test import override_settings
from django.test.client import RequestFactory
from lunch.api.serializers import ReceiptModelSerializer
from google_places_api.api import GooglePlaceDetail
from config.storage_backends import PrivateMediaStorage


@pytest.mark.django_db
def test_serializer(receipt_input_data, receipt_data):
    serializer = ReceiptModelSerializer(data=receipt_input_data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
@mock.patch("lunch.services.GooglePlacesAPI.place_details")
@mock.patch("lunch.services.GooglePlacesAPI.find_place_id")
def test_serializer__create(
    mocked_place_id,
    mocked_place_details,
    receipt_input_data,
    user,
    google_place_detail,
):
    mocked_place_id.return_value = "test"
    mocked_place_details.return_value = GooglePlaceDetail(google_place_detail["result"])

    request = RequestFactory()
    request.user = user
    serializer = ReceiptModelSerializer(
        data=receipt_input_data, context={"request": request}
    )

    assert serializer.is_valid() is True
    instance = serializer.create(serializer.validated_data)
    assert instance is not None

    ser = ReceiptModelSerializer(instance=instance)
    assert ser.data["image"] == instance.image.url


@override_settings(USE_S3=True)
def test_serializer_handle_image_upload():
    ser = ReceiptModelSerializer()
    ser._handle_image_upload()
    assert isinstance(ser.Meta.model.image.field.storage, PrivateMediaStorage)
