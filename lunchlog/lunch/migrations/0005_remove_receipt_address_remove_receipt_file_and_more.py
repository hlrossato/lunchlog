# Generated by Django 5.0.6 on 2024-07-02 08:57

import config.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lunch", "0004_alter_receipt_uuid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="receipt",
            name="address",
        ),
        migrations.RemoveField(
            model_name="receipt",
            name="file",
        ),
        migrations.AddField(
            model_name="receipt",
            name="image",
            field=models.ImageField(
                default=None,
                storage=config.storage_backends.PrivateMediaStorage(),
                upload_to="",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="receipt",
            name="restaurant_address",
            field=models.CharField(
                default=None, max_length=250, verbose_name="Restaurant Address"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="receipt",
            name="date",
            field=models.DateField(auto_now_add=True, verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="receipt",
            name="restaurant_name",
            field=models.CharField(max_length=100, verbose_name="Restaurant Name"),
        ),
    ]
