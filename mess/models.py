from django.db import models

MEAL_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('snacks', 'Snacks'),
    ('dinner', 'Dinner'),
]

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date = models.DateField() 
    description = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.date} - {self.meal_type} - {self.name}"

    class Meta:
        ordering = ['date', 'meal_type'] 


class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField()         
    comment = models.TextField(blank=True)
    student_name = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} rated {self.menu_item} - {self.stars}★"