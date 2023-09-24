import traceback
from uuid import uuid4 as uuid
from django.shortcuts import render

# Create your views here.
from application.models import Invoice, InvoiceDetails
from application.serializers import InvoiceSerializer, InvoiceDetailsSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ModelAPIView(APIView):

    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response, dict):
            if response["status"] == 1:
                del response["status"]
                response = Response(response, status=status.HTTP_200_OK)
            else:
                del response["status"]
                response = Response(response, status=status.HTTP_400_BAD_REQUEST)
        return super(ModelAPIView, self).finalize_response(
            request, response, *args, **kwargs
        )

    def handle_exception(self, exc):
        try:
            return super(ModelAPIView, self).handle_exception(exc)
        except Exception as ex:
            tb = traceback.format_exc()
            print(f"Exception in : {tb}, {ex}")
            return Response(
                {"msg": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InvoiceAPI(ModelAPIView):
    def get(self, request):
        """
        Get all invoices or particular invoice as per query parameters.

        Args:
            request (_type_): _description_
        """
        invoices = Invoice.objects.all()
        if request.GET:
            invoices = invoices.filter(**{field: request.GET[field] for field in request.GET if request.GET})
        serializer = InvoiceSerializer(data=list(invoices.values()), many=True)
        if serializer.is_valid():
            return {'status': 1, 'invoices': serializer.data}
        print(serializer.errors)
        return {'status': 0, 'msg': "Bad Request"}
    
    def post(self, request):
        """
        POST request to create new invoice object.

        Args:
            request (_type_): _description_
        """
        data = request.data
        data["invoice_number"] = uuid()
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return {'status': 1, 'invoice': serializer.data}
        print(serializer.errors)
        return {'status': 0, 'msg': "Bad Request"}

class InvoiceDetailsAPI(ModelAPIView):
    """
    Get all invoice details associated with an invoice or a customer.

    Args:
        APIView (_type_): _description_
    """
    def get(self, request):
        invoice_details = InvoiceDetails.objects.all()
        if request.GET:
            invoice_details = InvoiceDetails.objects.filter(**{field:request.GET[field] for field in request.GET})
        serializer = InvoiceDetailsSerializer(data=list(invoice_details.values()), many=True)
        if serializer.is_valid():
            return {'status': 1, "invoice_details": serializer.data}
        print(serializer.errors)
        return {"status": 0, "msg": "Bad Request"}
