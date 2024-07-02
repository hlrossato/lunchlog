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
        month = self.request.query_params.get("month")
        if month:
            queryset = Receipt.objects.filter(date__month=month)
        else:
            queryset = Receipt.objects.all()

        return queryset


class ReceiptDetailAPIView(ReceiptMixin, RetrieveUpdateDestroyAPIView):
    lookup_field = "uuid"
    queryset = Receipt.objects.all()
