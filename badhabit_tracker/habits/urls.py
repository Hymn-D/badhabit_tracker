# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HabitViewSet, HabitLogViewSet, ReplacementPlanViewSet,
    RegisterView, logout_view, ReportsView, UserHabitsSummaryView

)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")
router.register(r"logs", HabitLogViewSet, basename="habitlog")
router.register(r"plans", ReplacementPlanViewSet, basename="replacementplan")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", logout_view, name="logout"),
    path("reports/summary/", ReportsView.as_view(), name="reports-summary"),
    path('reports/habits/summary/', UserHabitsSummaryView.as_view(), name='user-habits-summary'),
    path("", include(router.urls)),
]
