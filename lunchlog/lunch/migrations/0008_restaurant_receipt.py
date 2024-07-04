# Generated by Django 5.0.6 on 2024-07-04 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lunch", "0007_restaurant_alter_receipt_date_alter_receipt_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="receipt",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="lunch.receipt",
            ),
        ),
    ]
