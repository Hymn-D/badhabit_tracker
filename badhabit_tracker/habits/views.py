from django.shortcuts import render
from django.db.models import Count, Sum, Max
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Habit, HabitLog, ReplacementPlan, Achievement, ActivityShare
from .serializers import (
    HabitSerializer, HabitLogSerializer, ReplacementPlanSerializer,RegisterSerializer, UserSerializer, AchievementSerializer, ActivityShareSerializer
)
from datetime import timedelta, date
from .utils import today_utc_date, start_of_week, start_of_month, daterange, compute_streaks, safe_percent_change


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# Habit viewset (user-scoped)
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # custom nested create for logs via /api/habits/{id}/logs/
    @action(detail=True, methods=['get', 'post'], url_path='logs')
    def logs(self, request, pk=None):
        habit = self.get_object()
        if request.method == 'GET':
            qs = habit.logs.all().order_by('-log_date')
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = HabitLogSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = HabitLogSerializer(qs, many=True)
            return Response(serializer.data)
        else:  # POST
            data = request.data.copy()
            serializer = HabitLogSerializer(data=data)
            if serializer.is_valid():
                # ensure uniqueness - either create or update existing log_date
                log_date = serializer.validated_data['log_date']
                obj, created = HabitLog.objects.get_or_create(habit=habit, log_date=log_date,
                                                              defaults={'occurrences': serializer.validated_data.get('occurrences',1),
                                                                        'note': serializer.validated_data.get('note','')})
                if not created:
                    # if exists, update fields
                    obj.occurrences = serializer.validated_data.get('occurrences', obj.occurrences)
                    obj.note = serializer.validated_data.get('note', obj.note)
                    obj.save()
                s = HabitLogSerializer(obj)
                return Response(s.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'], url_path='plans')
    def plans(self, request, pk=None):
        habit = self.get_object()
        if request.method == 'GET':
            qs = habit.plans.all()
            serializer = ReplacementPlanSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            data = request.data.copy()
            serializer = ReplacementPlanSerializer(data=data)
            if serializer.is_valid():
                # create plan linked to habit
                obj, created = ReplacementPlan.objects.get_or_create(habit=habit, activity=serializer.validated_data['activity'],
                                                                     defaults={'description': serializer.validated_data.get('description','')})
                s = ReplacementPlanSerializer(obj)
                return Response(s.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'], url_path='reminders')
    def reminders(self, request, pk=None):
        habit = self.get_object()
        if request.method == 'GET':
            qs = habit.reminders.all()
            serializer = ReminderSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            data = request.data.copy()
            serializer = ReminderSerializer(data=data)
            if serializer.is_valid():
                obj = Reminder.objects.create(habit=habit,
                                              reminder_time=serializer.validated_data['reminder_time'],
                                              message=serializer.validated_data.get('message','Stay strong 💪'))
                s = ReminderSerializer(obj)
                return Response(s.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'], url_path='report', permission_classes=[permissions.IsAuthenticated])
    def report(self, request, pk=None):
        """
        Returns aggregates & streaks for the habit:
        - daily_count (today)
        - weekly_count (current week)
        - monthly_count (current month)
        - last_30_days: list of {date, occurrences}
        - avg_daily_last_30: float
        - current_streak, longest_streak (in days)
        - total_logs
        """
        habit = self.get_object()
        today = today_utc_date()

        # ranges
        start_30 = today - timedelta(days=29)  # last 30 days includes today
        week_start = start_of_week(today)
        month_start = start_of_month(today)

        # Fetch logs in relevant range (past 365 days to compute streaks safely)
        earliest_needed = today - timedelta(days=365)
        logs_qs = HabitLog.objects.filter(habit=habit, log_date__gte=earliest_needed).order_by('log_date')

        # Build a map date -> occurrences (sum in case multiple entries, though we enforce uniqueness per day)
        occurrences_by_date = {}
        for log in logs_qs:
            d = log.log_date
            occurrences_by_date[d] = occurrences_by_date.get(d, 0) + (log.occurrences or 0)

        # Totals
        daily_count = occurrences_by_date.get(today, 0)
        weekly_count = sum(v for k, v in occurrences_by_date.items() if k >= week_start and k <= today)
        monthly_count = sum(v for k, v in occurrences_by_date.items() if k >= month_start and k <= today)
        total_logs = sum(occurrences_by_date.values())

        # last 30 days series
        last_30_series = []
        for d in daterange(start_30, today):
            last_30_series.append({"date": d.isoformat(), "occurrences": occurrences_by_date.get(d, 0)})

        # average daily in last 30 days
        total_last_30 = sum(item["occurrences"] for item in last_30_series)
        avg_daily_last_30 = total_last_30 / 30.0

        # streaks: compute set of dates where occurrences > 0
        dates_with_logs = {d for d, v in occurrences_by_date.items() if v > 0}
        current_streak, longest_streak = compute_streaks(dates_with_logs, upto_date=today)

        data = {
            "habit_id": habit.id,
            "habit_name": habit.name,
            "daily_count": daily_count,
            "weekly_count": weekly_count,
            "monthly_count": monthly_count,
            "total_occurrences": total_logs,
            "avg_daily_last_30": round(avg_daily_last_30, 2),
            "last_30_days": last_30_series,
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
        }
        return Response(data, status=status.HTTP_200_OK)


# Small viewsets for logs/plans/reminders so we can update/delete specific nested items
class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return HabitLog.objects.filter(habit__user=self.request.user)

    # override perform_create to ensure habit belongs to user when creating directly
    def perform_create(self, serializer):
        habit = serializer.validated_data.get('habit')
        if habit.user != self.request.user:
            raise PermissionError("Cannot create logs for this habit")
        serializer.save()

class ReplacementPlanViewSet(viewsets.ModelViewSet):
    serializer_class = ReplacementPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return ReplacementPlan.objects.filter(habit__user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Expects {"refresh": "<refresh_token>"} to blacklist (optional).
    If you do not configure token blacklist, client can just discard tokens.
    """
    try:
        refresh_token = request.data.get("refresh", None)
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # requires token_blacklist app
    except Exception:
        pass
    return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)


class ReportsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Summary across all user's habits: count habits, total logs, last log date per habit
        habits = Habit.objects.filter(user=request.user).annotate(
            total_logs=Count("logs"),
            last_log=Max("logs__log_date")
        ).values("id", "name", "category", "target_frequency", "total_logs", "last_log")
        return Response({"habits": list(habits)})

class UserHabitsSummaryView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        today = today_utc_date()
        week_start = start_of_week(today)
        month_start = start_of_month(today)

        habits = Habit.objects.filter(user=request.user)
        summary = []
        for habit in habits:
            # lightweight aggregates: total logs and last log date
            total_logs = HabitLog.objects.filter(habit=habit).aggregate(total=Sum('occurrences'))['total'] or 0
            last_log = HabitLog.objects.filter(habit=habit).order_by('-log_date').first()
            last_log_date = last_log.log_date.isoformat() if last_log else None

            summary.append({
                "habit_id": habit.id,
                "name": habit.name,
                "total_occurrences": total_logs,
                "last_log_date": last_log_date,
            })
        return Response({"habits": summary})


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)
    
class ReportsSummaryView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        today = today_utc_date()
        week_start = start_of_week(today)
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = week_start - timedelta(days=1)
        month_start = start_of_month(today)
        # prev month start naive:
        if month_start.month == 1:
            prev_month_start = month_start.replace(year=month_start.year-1, month=12)
        else:
            prev_month_start = month_start.replace(month=month_start.month-1)
        prev_month_end = month_start - timedelta(days=1)

        habits = Habit.objects.filter(user=user).order_by('-created_at')
        out = []
        for h in habits:
            logs = h.logs.all()
            occ_map = {}
            for l in logs:
                occ_map[l.log_date] = occ_map.get(l.log_date, 0) + (l.occurrences or 0)

            today_count = occ_map.get(today, 0)
            week_count = sum(v for d, v in occ_map.items() if d >= week_start and d <= today)
            prev_week_count = sum(v for d, v in occ_map.items() if d >= prev_week_start and d <= prev_week_end)
            month_count = sum(v for d, v in occ_map.items() if d >= month_start and d <= today)
            prev_month_count = sum(v for d, v in occ_map.items() if d >= prev_month_start and d <= prev_month_end)

            total = sum(occ_map.values())
            dates_with = {d for d, v in occ_map.items() if v > 0}
            current_streak, longest_streak = compute_streaks(dates_with, upto_date=today)

            out.append({
                "habit_id": h.id,
                "name": h.name,
                "today_count": today_count,
                "week_count": week_count,
                "week_percent_change": safe_percent_change(week_count, prev_week_count),
                "month_count": month_count,
                "month_percent_change": safe_percent_change(month_count, prev_month_count),
                "total_occurrences": total,
                "current_streak": current_streak,
                "longest_streak": longest_streak,
            })
        return Response({"habits": out})

# Habit analytics – detailed for single habit (last 30 days, streaks)
class HabitAnalyticsView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, habit_id):
        user = request.user
        habit = Habit.objects.filter(id=habit_id, user=user).first()
        if not habit:
            return Response({"detail": "Not found"}, status=404)

        today = today_utc_date()
        start_30 = today - timedelta(days=29)
        earliest = today - timedelta(days=365)
        logs = habit.logs.filter(log_date__gte=earliest).order_by('log_date')

        occ_map = {}
        for l in logs:
            occ_map[l.log_date] = occ_map.get(l.log_date, 0) + (l.occurrences or 0)

        last_30 = [{"date": d.isoformat(), "occurrences": occ_map.get(d, 0)} for d in daterange(start_30, today)]
        dates_with = {d for d, v in occ_map.items() if v > 0}
        current_streak, longest_streak = compute_streaks(dates_with, upto_date=today)

        # weekly/monthly counts
        week_start = start_of_week(today)
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = week_start - timedelta(days=1)

        week_count = sum(v for d, v in occ_map.items() if d >= week_start and d <= today)
        prev_week_count = sum(v for d, v in occ_map.items() if d >= prev_week_start and d <= prev_week_end)
        month_start = start_of_month(today)
        if month_start.month == 1:
            prev_month_start = month_start.replace(year=month_start.year-1, month=12)
        else:
            prev_month_start = month_start.replace(month=month_start.month-1)
        prev_month_end = month_start - timedelta(days=1)
        month_count = sum(v for d, v in occ_map.items() if d >= month_start and d <= today)
        prev_month_count = sum(v for d, v in occ_map.items() if d >= prev_month_start and d <= prev_month_end)

        data = {
            "habit_id": habit.id,
            "name": habit.name,
            "last_30_days": last_30,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "week_count": week_count,
            "week_percent_change": safe_percent_change(week_count, prev_week_count),
            "month_count": month_count,
            "month_percent_change": safe_percent_change(month_count, prev_month_count),
            "total_occurrences": sum(occ_map.values()),
        }
        return Response(data)

# Share an achievement (public or to user)
class AchievementShareView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivityShareSerializer

    def create(self, request, *args, **kwargs):
        achievement_id = kwargs.get("achievement_id")
        achievement = Achievement.objects.filter(id=achievement_id, user=request.user).first()
        if not achievement:
            return Response({"detail": "Achievement not found or not owned"}, status=404)
        data = request.data.copy()
        data["achievement"] = achievement.id
        data["user_from"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_from=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Generic activity share (can share habitlog or custom message)
class ActivityShareCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivityShareSerializer

    def perform_create(self, serializer):
        serializer.save(user_from=self.request.user)

# Leaderboard: Top users by total occurrences
class LeaderboardTopUsersView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        # annotate users with total occurrences across all their habits
        users = User.objects.all()
        leaderboard = []
        for u in users:
            total = HabitLog.objects.filter(habit__user=u).aggregate(total=Sum('occurrences'))['total'] or 0
            leaderboard.append({"user_id": u.id, "username": u.username, "total_occurrences": total})
        leaderboard.sort(key=lambda x: x["total_occurrences"], reverse=True)
        return Response({"leaderboard": leaderboard[:limit]})

# Leaderboard: Top current streaks (users)
class LeaderboardTopStreaksView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        today = today_utc_date()
        users = User.objects.all()
        out = []
        for u in users:
            # compute user's best current streak across their habits
            user_habits = Habit.objects.filter(user=u)
            best_current = 0
            for h in user_habits:
                dates_with = {l.log_date for l in h.logs.all() if (l.occurrences or 0) > 0}
                current_streak, _ = compute_streaks(dates_with, upto_date=today)
                if current_streak > best_current:
                    best_current = current_streak
            out.append({"user_id": u.id, "username": u.username, "current_streak": best_current})
        out.sort(key=lambda x: x["current_streak"], reverse=True)
        return Response({"leaderboard": out[:limit]})