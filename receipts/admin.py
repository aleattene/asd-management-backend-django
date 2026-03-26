from django.contrib import admin

from receipts.models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("date", "user", "description", "amount", "payment_method", "is_active")
    list_filter = ("is_active", "payment_method")
    search_fields = ("description", "user__last_name", "user__first_name")
    date_hierarchy = "date"
