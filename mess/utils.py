from django.utils import timezone
from .models import WeeklyMenu, MenuOverride

def get_todays_menu():
    today = timezone.now().date()
    day_of_week = today.weekday()  # 0=Monday, 6=Sunday
    
    meals = {}
    for meal_type in ['breakfast', 'lunch', 'snacks', 'dinner']:

        # Check if there's an override for today first
        override = MenuOverride.objects.filter(
            date=today, meal_type=meal_type
        ).first()

        if override:
            meals[meal_type] = {
                'name': override.name,
                'description': override.description,
                'is_override': True,   # we can show a "special menu" badge
            }
        else:
            # Fall back to weekly schedule
            weekly = WeeklyMenu.objects.filter(
                day_of_week=day_of_week, meal_type=meal_type
            ).first()

            if weekly:
                meals[meal_type] = {
                    'name': weekly.name,
                    'description': weekly.description,
                    'is_override': False,
                }
            else:
                meals[meal_type] = None  # no menu set

    return today, meals