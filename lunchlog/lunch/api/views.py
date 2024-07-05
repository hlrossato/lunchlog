from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from lunch.api.serializers import ReceiptModelSerializer
from lunch.models import Receipt


class ReceiptMixin:
    serializer_class = ReceiptModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class ReceiptAPIView(ReceiptMixin, ListCreateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        print(self.request.query_params)
        month = self.request.query_params.get("month")
        queryset = Receipt.objects.filter(user=self.request.user)

        if month:
            queryset = queryset.filter(date__month=month)

        return queryset


class ReceiptDetailAPIView(ReceiptMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "uuid"

    def get_queryset(self):
        return Receipt.objects.filter(user=self.request.user)
