from django.db import models


class Address(models.Model):
    street_name = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True
