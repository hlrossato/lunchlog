import uuid
from datetime import datetime, timezone
from typing import Self

from django.db import models

from common.models import Address
from lunch.services import populate_restaurant


def user_directory_path(instance: "Receipt", filename: str) -> str:
    # file will be uploaded to MEDIA_ROOT/user_<id>/<date>/<filename>
    now = datetime.now(timezone.utc).date()
    return f"user_{instance.user.id}/{now.strftime("%Y/%m/%d")}/{filename}"


class Receipt(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    restaurant_name = models.CharField(max_length=100)
    restaurant_address = models.CharField(max_length=250)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)

    class Meta:
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def save(self: Self, *args: tuple, **kwargs: dict) -> None:
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            populate_restaurant(self)


class Restaurant(Address):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    place_id = models.CharField(max_length=100)
    formatted_address = models.CharField(max_length=250, blank=True, null=True)
    serves_beer = models.BooleanField(default=False, null=True)
    serves_breakfast = models.BooleanField(default=False, null=True)
    serves_brunch = models.BooleanField(default=False, null=True)
    serves_dinner = models.BooleanField(default=False, null=True)
    serves_lunch = models.BooleanField(default=False, null=True)
    serves_vegetarian_food = models.BooleanField(default=False, null=True)
    serves_wine = models.BooleanField(default=False, null=True)
    takeout = models.BooleanField(default=False, null=True)
    delivery = models.BooleanField(default=False, null=True)
    opening_hours = models.JSONField()

    receipt = models.ForeignKey("lunch.Receipt", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
