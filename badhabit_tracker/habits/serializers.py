from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Habit, HabitLog, ReplacementPlan, Achievement, ActivityShare

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ("id", "habit", "log_date", "occurrences", "note", "created_at")
        read_only_fields = ("created_at", "id", "habit")


class ReplacementPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplacementPlan
        fields = ("id", "habit", "activity", "description", "created_at")
        read_only_fields = ("created_at", "id", "habit")

class HabitSerializer(serializers.ModelSerializer):
    logs = HabitLogSerializer(many=True, read_only=True)
    plans = ReplacementPlanSerializer(many=True, read_only=True)
    class Meta:
        model = Habit
        fields = ("id", "user", "name", "category", "description", "target_frequency", "created_at", "is_active",
                  "logs", "plans", "reminders", "journal_entries")
        read_only_fields = ("id", "user", "created_at", "logs", "plans", "reminders", "journal_entries")

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ("id", "user", "name", "description", "earned_at")
        read_only_fields = ("id", "user", "earned_at")

class ActivityShareSerializer(serializers.ModelSerializer):
    user_from = serializers.ReadOnlyField(source='user_from.id')
    user_from_username = serializers.ReadOnlyField(source='user_from.username')
    user_to_username = serializers.ReadOnlyField(source='user_to.username')

    class Meta:
        model = ActivityShare
        fields = ("id", "user_from", "user_from_username", "user_to", "user_to_username",
                  "achievement", "habitlog", "message", "is_public", "external_url", "created_at")
        read_only_fields = ("id", "user_from", "created_at")

class LeaderboardUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    total_occurrences = serializers.IntegerField()
    current_streak = serializers.IntegerField(required=False)
