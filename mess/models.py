from django.db import models

MEAL_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('snacks', 'Snacks'),
    ('dinner', 'Dinner'),
]

DAY_CHOICES = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]

class WeeklyMenu(models.Model):
    """Default repeating weekly schedule"""
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    name = models.CharField(max_length=200)        # e.g. "Idli Sambar, Vada"
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['day_of_week', 'meal_type']
        unique_together = ['day_of_week', 'meal_type']  # one menu per day per meal

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.meal_type} - {self.name}"


class MenuOverride(models.Model):
    """One-off override for a specific date when menu changes"""
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'meal_type']
        unique_together = ['date', 'meal_type']    # one override per date per meal

    def __str__(self):
        return f"OVERRIDE {self.date} - {self.meal_type} - {self.name}"


class Rating(models.Model):
    """Student ratings — linked to a specific date + meal"""
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date = models.DateField(auto_now_add=True)      # ← add auto_now_add=True
    stars = models.IntegerField()
    comment = models.TextField(blank=True)
    student_name = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student_name} - {self.meal_type} {self.date} - {self.stars}★"