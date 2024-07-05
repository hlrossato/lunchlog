from django.conf import settings
from rest_framework import serializers
from lunch.models import Receipt
from config.storage_backends import PrivateMediaStorage


class ReceiptModelSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%y")
    price = serializers.DecimalField(max_digits=5, decimal_places=2)

    def _handle_image_upload(self):
        # Handle file upload locally
        # I'm not sure if this is the best approach but was the one I've found
        if settings.USE_S3:
            self.Meta.model.image.field.storage = PrivateMediaStorage()

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        self._handle_image_upload()
        return super().create(validated_data)

    class Meta:
        model = Receipt
        exclude = ["id", "user"]
