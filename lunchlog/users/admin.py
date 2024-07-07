from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    """Admin View for User"""

    list_display = ("email", "first_name", "last_name", "email", "is_superuser")
    list_filter = ("is_active", "is_superuser", "is_staff")
    search_fields = ("email",)
