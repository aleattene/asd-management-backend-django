from django.contrib import admin

from companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("business_name", "vat_number", "fiscal_code", "vat_equals_fc", "is_active")
    list_filter = ("is_active", "vat_equals_fc")
    search_fields = ("business_name", "vat_number", "fiscal_code")
