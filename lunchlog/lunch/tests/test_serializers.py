import pytest
from django.test.client import RequestFactory
from lunch.api.serializers import ReceiptModelSerializer


@pytest.mark.django_db
def test_serializer(receipt_input_data, receipt_data):
    serializer = ReceiptModelSerializer(data=receipt_input_data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_serializer__create(receipt_input_data, user):
    request = RequestFactory()
    request.user = user
    serializer = ReceiptModelSerializer(
        data=receipt_input_data, context={"request": request}
    )

    assert serializer.is_valid() is True
    instance = serializer.create(serializer.validated_data)
    assert instance is not None

    ser = ReceiptModelSerializer(instance=instance)
    assert ser.get_image_url(instance) == instance.image.url
