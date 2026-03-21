from django.contrib import admin

from .models import Athlete, Category


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "fiscal_code",
        "category",
        "trainer",
        "is_active",
    )
    list_filter = ("category", "is_active", "trainer")
    search_fields = ("first_name", "last_name", "fiscal_code")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "age_range", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "description")
