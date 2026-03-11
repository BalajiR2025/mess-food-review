from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Avg
from .models import WeeklyMenu, MenuOverride, Rating
from .utils import get_todays_menu, get_meal_status

MEAL_ORDER = ['breakfast', 'lunch', 'snacks', 'dinner']

def home(request):
    today, meals = get_todays_menu()

    meal_data = {}
    for meal_type in MEAL_ORDER:
        menu = meals.get(meal_type)
        if menu:
            ratings = Rating.objects.filter(meal_type=meal_type, date=today)
            avg = ratings.aggregate(Avg('stars'))['stars__avg']
            count = ratings.count()
            all_comments = ratings.exclude(comment='').values('student_name', 'comment', 'stars')

            status, time_info = get_meal_status(meal_type)

            meal_data[meal_type] = {
                'name': menu['name'],
                'description': menu['description'],
                'is_override': menu['is_override'],
                'avg_rating': round(avg, 1) if avg else None,
                'rating_count': count,
                'comments': list(all_comments),
                'status': status,        # 'upcoming', 'open', 'closed'
                'time_info': time_info,  # open time or close time
            }
        else:
            meal_data[meal_type] = None

    return render(request, 'mess/home.html', {
        'meal_data': meal_data,
        'today': today,
        'meal_order': MEAL_ORDER,
    })


def rate_meal(request, meal_type):
    today, meals = get_todays_menu()
    menu = meals.get(meal_type)

    if not menu:
        return redirect('home')

    # Block rating if window is not open
    status, _ = get_meal_status(meal_type)
    if status != 'open':
        return redirect('home')

    rated_key = f'rated_{meal_type}_{today}'
    already_rated = request.session.get(rated_key, False)

    if request.method == 'POST' and not already_rated:
        stars = int(request.POST.get('stars'))
        comment = request.POST.get('comment', '')
        student_name = request.POST.get('student_name', '').strip()

        if student_name and 1 <= stars <= 5:
            Rating.objects.create(
                meal_type=meal_type,
                date=today,
                stars=stars,
                comment=comment,
                student_name=student_name
            )
            request.session[rated_key] = True

        return redirect('home')

    return render(request, 'mess/rate.html', {
        'meal_type': meal_type,
        'menu': menu,
        'today': today,
        'already_rated': already_rated,
    })