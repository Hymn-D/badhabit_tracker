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


class Achievement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="achievements", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ("-earned_at",)

    def __str__(self):
        return f"{self.name} ({self.user})"
    
class ActivityShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_activities")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="shares", null=True, blank=True)
    shared_to = models.CharField(max_length=255, null=True, blank=True)  # e.g., "Twitter", "Instagram", or a username
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} shared {self.achievement.name if self.achievement else 'an activity'}"

class Reminder(models.Model):
    id = models.AutoField(primary_key=True)
    habit = models.ForeignKey(Habit, related_name="reminders", on_delete=models.CASCADE)
    reminder_time = models.TimeField()
    message = models.CharField(max_length=255, default="Stay strong 💪")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Reminder {self.habit.name} @ {self.reminder_time}"


class JournalEntry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="journal_entries", on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, related_name="journal_entries", on_delete=models.SET_NULL, null=True, blank=True)
    entry = models.TextField()
    mood = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Journal by {self.user} @ {self.created_at}"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # e.g., emoji or icon path

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='users')
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user} - {self.badge.name}"