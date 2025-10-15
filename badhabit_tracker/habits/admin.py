from django.contrib import admin
from django.contrib import admin
from .models import (
    Habit,
    HabitLog,
    ReplacementPlan,
    Achievement,
    ActivityShare,
)

# Customize display in the admin panel for each model
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
