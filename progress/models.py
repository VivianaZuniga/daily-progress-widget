from django.db import models
from django.utils import timezone

class Activity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DailyLog(models.Model):
    date = models.DateField(default=timezone.now)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='records')
    complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'activity')

    def __str__(self):
        return f"{self.date} - {self.activity.name} - {'V' if self.complete else 'F'}"