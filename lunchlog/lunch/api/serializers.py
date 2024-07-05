from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from lunch.models import Receipt


class ReceiptModelSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d/%m/%y")
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)

    def get_image_url(self, obj: Receipt) -> str:
        return obj.image.url

    def _handle_image_upload(self):
        # Handling file upload locally
        if not settings.USE_S3:
            self.Meta.model.image.field.storage = FileSystemStorage()

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        self._handle_image_upload()
        return super().create(validated_data)

    class Meta:
        model = Receipt
        exclude = ["id", "user"]
