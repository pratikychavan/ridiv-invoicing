# Generated by Django 4.2.2 on 2023-09-24 03:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="invoicedetails",
            old_name="invoice_num",
            new_name="invoice",
        ),
    ]
