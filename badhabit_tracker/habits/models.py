from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Habit(models.Model):
    CATEGORY_CHOICES = [
        ("health", "Health"),
        ("finance", "Finance"),
        ("productivity", "Productivity"),
        ("other", "Other"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="habits", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    description = models.TextField(blank=True, null=True)
    target_frequency = models.IntegerField(default=0)  # number of occurrences expected
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} ({self.user})"


class HabitLog(models.Model):
    id = models.AutoField(primary_key=True)
    habit = models.ForeignKey(Habit, related_name="logs", on_delete=models.CASCADE)
    log_date = models.DateField()  # date of the log
    occurrences = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("habit", "log_date")
        ordering = ("-log_date",)

    def __str__(self):
        return f"Log {self.habit.name} @ {self.log_date}"


class ReplacementPlan(models.Model):
    id = models.AutoField(primary_key=True)
    habit = models.ForeignKey(Habit, related_name="plans", on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("habit", "activity")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.activity} for {self.habit.name}"