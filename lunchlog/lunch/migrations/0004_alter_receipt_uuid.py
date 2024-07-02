# Generated by Django 5.0.6 on 2024-07-01 12:38

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lunch", "0003_receipt_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, verbose_name="UUID"
            ),
        ),
    ]
