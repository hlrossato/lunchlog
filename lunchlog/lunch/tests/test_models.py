import pytest
from lunch.models import Receipt


@pytest.mark.django_db
def test_receipt__created(receipt_data):
    receipt = Receipt.objects.create(**receipt_data)
    assert receipt is not None
