from django.db import models

class Schedule(models.Model):
    SCHEDULE_TYPES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    platform = models.CharField(max_length=100)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date}"