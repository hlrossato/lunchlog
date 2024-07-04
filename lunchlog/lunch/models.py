import uuid
from django.db import models

from config.storage_backends import PrivateMediaStorage


class Receipt(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False)
    date = models.DateField(verbose_name="Date")
    price = models.DecimalField(verbose_name="Price", max_digits=5, decimal_places=2)
    restaurant_name = models.CharField(verbose_name="Restaurant Name", max_length=100)
    restaurant_address = models.CharField(
        verbose_name="Restaurant Address", max_length=250
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    image = models.ImageField(storage=PrivateMediaStorage())

    class Meta:
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"
