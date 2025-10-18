from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Habit, HabitLog, Badge, UserBadge

def award_badge(user, badge_name, description):
    badge, _ = Badge.objects.get_or_create(name=badge_name, defaults={'description': description})
    UserBadge.objects.get_or_create(user=user, badge=badge)

@receiver(post_save, sender=Habit)
def on_habit_created(sender, instance, created, **kwargs):
    if created:
        award_badge(instance.user, "First Habit Created", "Congratulations! You created your first habit 🎉")

@receiver(post_save, sender=HabitLog)
def on_habit_log_created(sender, instance, created, **kwargs):
    if created:
        count = HabitLog.objects.filter(habit__user=instance.habit.user).count()
        if count == 7:
            award_badge(instance.habit.user, "One Week Streak", "You logged habits for 7 days straight! 💪")
