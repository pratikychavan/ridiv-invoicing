
from rest_framework import serializers

from application.models import Invoice, InvoiceDetails


from rest_framework import serializers
from .models import Invoice, InvoiceDetails

class InvoiceDetailsSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
    quantity = serializers.DecimalField(max_digits=5, decimal_places=2)
    unit_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)

    def create(self, validated_data):
        quantity = validated_data.get('quantity')
        unit_price = validated_data.get('unit_price')
        price = quantity * unit_price
        return InvoiceDetails.objects.create(price=price, **validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.price = instance.quantity * instance.unit_price
        instance.save()
        return instance

class InvoiceSerializer(serializers.Serializer):
    created_date = serializers.DateTimeField(required=False)
    invoice_number = serializers.UUIDField()
    customer_name = serializers.CharField(max_length=255)
    invoice_details = InvoiceDetailsSerializer(many=True, required=False)       # Nested serializer for details

    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details', [])        # Extract invoice details data\
        invoice = Invoice.objects.create(**validated_data)                      # Create the invoice
        for detail_data in invoice_details_data:
            InvoiceDetails.objects.create(invoice=invoice, **detail_data)   # Create associated invoice details

        return invoice

    def update(self, instance, validated_data):
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        # Update associated invoice details
        invoice_details_data = validated_data.get('invoice_details', [])
        existing_details = instance.invoicedetails_set.all()
        for detail_data in invoice_details_data:
            detail_id = detail_data.get('id')
            if detail_id:
                detail = existing_details.filter(id=detail_id).first()
                if detail:
                    detail.description = detail_data.get('description', detail.description)
                    detail.quantity = detail_data.get('quantity', detail.quantity)
                    detail.unit_price = detail_data.get('unit_price', detail.unit_price)
                    detail.save()
            else:
                InvoiceDetails.objects.create(invoice=instance, **detail_data)

        return instance
