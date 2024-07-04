# Generated by Django 5.0.6 on 2024-07-04 12:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_customuser_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("6b474f7c-2015-42e2-b494-efdf003d0e0f"),
                editable=False,
                verbose_name="UUID",
            ),
        ),
    ]
