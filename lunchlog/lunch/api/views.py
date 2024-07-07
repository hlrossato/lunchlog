from typing import Any, TYPE_CHECKING, Dict, Self

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from lunch.api.serializers import ReceiptModelSerializer
from lunch.models import Receipt

if TYPE_CHECKING:
    from django.db.models.query import QuerySet  # pragma: no cover


class ReceiptMixin:
    serializer_class = ReceiptModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ReceiptAPIView(ReceiptMixin, ListCreateAPIView):
    def get_serializer_context(self: Self) -> Dict[Any, Any]:
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self: Self) -> "QuerySet[Receipt]":
        month = self.request.query_params.get("month")
        queryset = Receipt.objects.filter(user=self.request.user)

        if month:
            queryset = queryset.filter(date__month=month)

        return queryset


class ReceiptDetailAPIView(ReceiptMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "uuid"

    def get_queryset(self: Self) -> "QuerySet[Receipt]":
        return Receipt.objects.filter(user=self.request.user)
