# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HabitViewSet, HabitLogViewSet, ReplacementPlanViewSet,
    RegisterView, logout_view, ReportsView, UserHabitsSummaryView, AchievementViewSet, ReportsSummaryView, HabitAnalyticsView,
    AchievementShareView, ActivityShareCreateView,
    LeaderboardTopUsersView, LeaderboardTopStreaksView, ReminderViewSet, JournalEntryViewSet, BadgeViewSet, UserBadgeViewSet

)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")
router.register(r"logs", HabitLogViewSet, basename="habitlog")
router.register(r"plans", ReplacementPlanViewSet, basename="replacementplan")
router.register(r"achievements", AchievementViewSet, basename="achievement")
router.register(r'reminders', ReminderViewSet, basename='reminders')
router.register(r'journal', JournalEntryViewSet, basename='journal')
router.register(r'badges', BadgeViewSet, basename='badges')
router.register(r'user-badges', UserBadgeViewSet, basename='user-badges')

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", logout_view, name="logout"),
    path("reports/summary/", ReportsView.as_view(), name="reports-summary"),
    path('reports/habits/summary/', UserHabitsSummaryView.as_view(), name='user-habits-summary'),
    path("reports/summary/", ReportsSummaryView.as_view(), name="reports-summary"),
    path("habits/<int:habit_id>/analytics/", HabitAnalyticsView.as_view(), name="habit-analytics"),
    path("achievements/<int:achievement_id>/share/", AchievementShareView.as_view(), name="achievement-share"),
    path("activity/share/", ActivityShareCreateView.as_view(), name="activity-share"),
    path("leaderboards/top-users/", LeaderboardTopUsersView.as_view(), name="leaderboard-top-users"),
    path("leaderboards/top-streaks/", LeaderboardTopStreaksView.as_view(), name="leaderboard-top-streaks"),
    path("", include(router.urls)),
]
