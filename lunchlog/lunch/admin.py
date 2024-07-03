from lunch.models import Receipt
from django.contrib import admin


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    """Admin View for Receipt"""

    list_display = ("restaurant_name",)
    # list_filter = ("",)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ("",)
    # readonly_fields = ("",)
    # search_fields = ("",)
    # date_hierarchy = ""
    # ordering = ("",)
