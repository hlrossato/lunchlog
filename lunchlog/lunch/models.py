import uuid
from django.db import models

from lunchlog.storage_backends import PrivateMediaStorage


class Receipt(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name="Date", auto_now=False, auto_now_add=True)
    price = models.DecimalField(verbose_name="Price", max_digits=5, decimal_places=2)
    restaurant_name = models.CharField(verbose_name="Restaurant", max_length=100)
    address = models.CharField(verbose_name="Address", max_length=250)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    file = models.FileField(storage=PrivateMediaStorage())

    class Meta:
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def __str__(self):
        pass
