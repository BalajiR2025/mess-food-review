from django.contrib import admin
from .models import WeeklyMenu, MenuOverride, Rating

@admin.register(WeeklyMenu)
class WeeklyMenuAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'meal_type', 'name', 'description']
    list_filter = ['day_of_week', 'meal_type']
    ordering = ['day_of_week', 'meal_type']

@admin.register(MenuOverride)
class MenuOverrideAdmin(admin.ModelAdmin):
    list_display = ['date', 'meal_type', 'name', 'description']
    list_filter = ['meal_type', 'date']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'meal_type', 'date', 'stars', 'submitted_at']
    list_filter = ['stars', 'meal_type']
    search_fields = ['student_name']