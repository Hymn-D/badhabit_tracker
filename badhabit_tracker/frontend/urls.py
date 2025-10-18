from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('habits/', views.habit_view, name='habits'),
    path('reminders/', views.reminders_view, name='reminders'),
    path('reports/', views.reports_view, name='reports'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('journal/', views.journal_view, name='journal'),
]

