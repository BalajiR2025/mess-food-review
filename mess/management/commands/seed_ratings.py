import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from mess.models import Rating

NAMES = ["Arjun", "Priya", "Karthik", "Divya", "Rahul", "Sneha", "Vignesh", "Anu"]
MEALS = ['breakfast', 'lunch', 'snacks', 'dinner']

class Command(BaseCommand):
    help = "Seed last 7 days with sample ratings for demo purposes"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        created = 0
        for i in range(7):
            day = today - timedelta(days=i)
            for meal in MEALS:
                for _ in range(random.randint(2, 5)):
                    Rating.objects.create(
                        meal_type=meal,
                        date=day,
                        stars=random.randint(3, 5),
                        comment=random.choice(["Good", "Could be better", "", "Loved it!"]),
                        student_name=random.choice(NAMES),
                        roll_number=f"22CS0{random.randint(10,99)}",
                        room_number=f"B-{random.randint(100,305)}",
                    )
                    created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} demo ratings"))