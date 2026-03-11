from django.utils import timezone
from .models import WeeklyMenu, MenuOverride
from datetime import time

def get_todays_menu():
    today = timezone.now().date()
    day_of_week = today.weekday()  # 0=Monday, 6=Sunday
    
    meals = {}
    for meal_type in ['breakfast', 'lunch', 'snacks', 'dinner']:
        override = MenuOverride.objects.filter(
            date=today, meal_type=meal_type
        ).first()

        if override:
            meals[meal_type] = {
                'name': override.name,
                'description': override.description,
                'is_override': True,
            }
        else:
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
                meals[meal_type] = None

    return today, meals


# Meal timing windows
MEAL_TIMES = {
    'breakfast': (time(7, 0),  time(10, 30)),
    'lunch':     (time(12, 0), time(14, 30)),
    'snacks':    (time(16, 0), time(18, 30)),
    'dinner':    (time(19, 0), time(21, 30)),
}

def get_meal_status(meal_type):
    """
    Returns:
      'upcoming'  → before meal time
      'open'      → rating window is open
      'closed'    → meal time passed
    """
    now = timezone.localtime(timezone.now()).time()
    start, end = MEAL_TIMES.get(meal_type, (time(0, 0), time(23, 59)))

    if now < start:
        return 'upcoming', start.strftime('%I:%M %p')
    elif start <= now <= end:
        return 'open', end.strftime('%I:%M %p')
    else:
        return 'closed', None