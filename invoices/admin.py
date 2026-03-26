from django.contrib import admin

from invoices.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("number", "date", "company", "direction", "amount", "payment_method", "is_active")
    list_filter = ("direction", "is_active", "payment_method")
    search_fields = ("number", "description", "company__business_name")
    date_hierarchy = "date"
