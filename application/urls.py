from django.urls import path
from application.views import InvoiceAPI, InvoiceDetailsAPI

urlpatterns = [
    path("invoice/", InvoiceAPI.as_view(), name="invoice"),
    path("invoice_details/", InvoiceDetailsAPI.as_view(), name="invoice_details")
]