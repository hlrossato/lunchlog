from typing import Self, Any
from django.conf import settings
from rest_framework import serializers
from lunch.models import Receipt
from config.storage_backends import PrivateMediaStorage


class ReceiptModelSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%y")
    price = serializers.DecimalField(max_digits=5, decimal_places=2)

    def _handle_image_upload(self: Self) -> None:
        """
        Handle image upload by setting S3 storage if/when USE_S3 flag is true
        """

        if settings.USE_S3:
            # I'm not sure if this is the best approach but was the one I've found
            self.Meta.model.image.field.storage = PrivateMediaStorage()

    def create(self: Self, validated_data: dict) -> Any:
        validated_data["user"] = self.context["request"].user
        self._handle_image_upload()
        return super().create(validated_data)

    class Meta:
        model = Receipt
        exclude = ["id", "user"]
