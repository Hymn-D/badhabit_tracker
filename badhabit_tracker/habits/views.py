from django.shortcuts import render
from django.db.models import Count, Sum, Max
from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Habit, HabitLog, ReplacementPlan
from .serializers import (
    HabitSerializer, HabitLogSerializer, ReplacementPlanSerializer,   RegisterSerializer, UserSerializer
)

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