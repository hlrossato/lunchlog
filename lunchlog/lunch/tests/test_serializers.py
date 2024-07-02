import pytest
from lunch.api.serializers import ReceiptModelSerializer


@pytest.mark.django_db
def test_serializer(receipt_input_data, receipt_data):
    serializer = ReceiptModelSerializer(data=receipt_input_data)
    assert serializer.is_valid() is True
