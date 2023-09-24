from django.db import models

# Create your models here.

# Invoice model fields -> Date, Invoice No, CustomerName.
class Invoice(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.UUIDField(unique=True, null=True)   
    customer_name = models.CharField(max_length=255)

# InvoiceDetail model fields -> invoice (ForeignKey), description, quantity, unit_price, price.
class InvoiceDetails(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, to_field="invoice_number", null=True
    )
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(null=True, default=0)
    unit_price = models.FloatField(null=True, default=0)
    price = models.FloatField(null=True, default=0)

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.unit_price
        super().save(*args, **kwargs)