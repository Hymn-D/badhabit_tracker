from django.contrib import admin
from django.contrib import admin
from .models import (
    Habit,
    HabitLog,
    ReplacementPlan,
    Achievement,
    ActivityShare,
    Reminder, 
    JournalEntry, 
    Badge, 
    UserBadge
)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "category", "target_frequency", "created_at")
    search_fields = ("name", "category", "user__username")
    list_filter = ("category", "created_at")
    ordering = ("-created_at",)


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("id", "habit", "log_date", "occurrences", "created_at")
    search_fields = ("habit__name",)
    list_filter = ("log_date",)
    ordering = ("-log_date",)


@admin.register(ReplacementPlan)
class ReplacementPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "habit", "activity", "created_at")
    search_fields = ("activity", "habit__name")
    ordering = ("-created_at",)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "earned_at")
    search_fields = ("user__username", "name")
    ordering = ("-earned_at",)


@admin.register(ActivityShare)
class ActivityShareAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "achievement", "shared_to", "shared_at")
    search_fields = ("user__username", "achievement__name", "shared_to")
    ordering = ("-shared_at",)

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('habit', 'reminder_time', 'message', 'created_at')
    list_filter = ('reminder_time',)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'habit', 'mood', 'created_at')
    search_fields = ('title', 'entry', 'user__username')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')