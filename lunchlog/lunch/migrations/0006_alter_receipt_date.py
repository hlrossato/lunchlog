# Generated by Django 5.0.6 on 2024-07-02 12:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lunch", "0005_remove_receipt_address_remove_receipt_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="date",
            field=models.DateField(verbose_name="Date"),
        ),
    ]
