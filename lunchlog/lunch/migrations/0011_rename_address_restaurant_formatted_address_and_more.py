# Generated by Django 5.0.6 on 2024-07-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lunch", "0010_restaurant_place_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="restaurant",
            old_name="address",
            new_name="formatted_address",
        ),
        migrations.AddField(
            model_name="restaurant",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="postal_code",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="state",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="street_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="street_number",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
