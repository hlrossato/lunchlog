from lunch.models import Receipt, Restaurant
from django.contrib import admin


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    """Admin View for Receipt"""

    list_display = ("restaurant_name", "user", "date")
    list_filter = ("restaurant_name", "user", "date")
    readonly_fields = ("user",)
    search_fields = ("restaurant_name", "restaurant_address")
    ordering = ("-date",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Admin View for Restaurant"""

    list_display = ("name", "receipt", "user")
    list_filter = (
        "name",
        "serves_beer",
        "serves_breakfast",
        "serves_brunch",
        "serves_dinner",
        "serves_lunch",
        "serves_vegetarian_food",
        "serves_wine",
        "takeout",
        "delivery",
    )
    readonly_fields = ("user", "receipt")
    search_fields = ("formatted_address",)
    ordering = ("-receipt__date",)
