from django.contrib import admin

from geography.models import Country, Province, Municipality


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "iso_code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "iso_code")


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
    list_filter = ("province",)
    search_fields = ("name",)
