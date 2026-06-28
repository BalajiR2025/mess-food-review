import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from mess.models import Rating

NAMES = ["Arjun", "Priya", "Karthik", "Divya", "Rahul", "Sneha", "Vignesh", "Anu", "Sanjay", "Meena"]
MEALS = ['breakfast', 'lunch', 'snacks', 'dinner']

GOOD_COMMENTS = ["Loved it!", "Tasted great", "Best meal this week", "Perfectly cooked", ""]
AVERAGE_COMMENTS = ["Okay", "Could be better", "Average taste", ""]
BAD_COMMENTS = ["Too salty", "Cold food", "Undercooked", "Not good at all", "Quality dropped", ""]

class Command(BaseCommand):
    help = "Seed last 7 days with sample ratings, including extreme good/bad cases"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        created = 0

        for i in range(7):
            day = today - timedelta(days=i)

            for meal in MEALS:
                # Randomly decide this meal's overall "mood" for the day
                # so ratings aren't just random noise — they reflect a realistic pattern
                mood = random.choices(
                    ['excellent', 'good', 'average', 'poor', 'terrible'],
                    weights=[15, 30, 30, 15, 10]  # mostly average/good, some extremes
                )[0]

                if mood == 'excellent':
                    star_pool = [5, 5, 5, 4]
                    comment_pool = GOOD_COMMENTS
                elif mood == 'good':
                    star_pool = [4, 4, 5, 3]
                    comment_pool = GOOD_COMMENTS
                elif mood == 'average':
                    star_pool = [3, 3, 4, 2]
                    comment_pool = AVERAGE_COMMENTS
                elif mood == 'poor':
                    star_pool = [2, 2, 1, 3]
                    comment_pool = BAD_COMMENTS
                else:  # terrible
                    star_pool = [1, 1, 1, 2]
                    comment_pool = BAD_COMMENTS

                num_ratings = random.randint(3, 7)
                for _ in range(num_ratings):
                    Rating.objects.create(
                        meal_type=meal,
                        date=day,
                        stars=random.choice(star_pool),
                        comment=random.choice(comment_pool),
                        student_name=random.choice(NAMES),
                        roll_number=f"22CS0{random.randint(10,99)}",
                        room_number=f"B-{random.randint(100,305)}",
                    )
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} demo ratings (with extreme cases included)"))