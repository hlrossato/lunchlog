from django.urls import path
from lunch.api import views

app_name = "lunch"

urlpatterns = [
    path("", views.ReceiptAPIView.as_view(), name="receipt"),
    path("<uuid>/", views.ReceiptDetailAPIView.as_view(), name="receipt-detail"),
]
