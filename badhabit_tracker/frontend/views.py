from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from habits.models import Habit, HabitLog, ReplacementPlan, Reminder, Achievement, JournalEntry
from datetime import date
from django.utils import timezone


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    habits = Habit.objects.filter(user=request.user, is_deleted=False)
    logs = HabitLog.objects.filter(habit__user=request.user).order_by('-log_date')[:10]
    achievements = Achievement.objects.filter(user=request.user)
    reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'habits': habits,
        'logs': logs,
        'achievements': achievements
    })


@login_required
def habit_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description', '')
        target_frequency = request.POST.get('target_frequency', 0)
        if name:
            Habit.objects.create(
                user=request.user,
                name=name,
                category=category,
                description=description,
                target_frequency=target_frequency
            )
            messages.success(request, f'Habit "{name}" added successfully!')
            return redirect('dashboard')
    return render(request, 'add_habit.html')


@login_required
def reports_view(request):
    habits = Habit.objects.filter(user=request.user,  is_deleted=False)
    reports: list = [] 
    data = []
    for habit in habits:
       logs = HabitLog.objects.filter(habit=habit)
       daily_count = logs.filter(date=timezone.now().date()).count()
       weekly_count = logs.filter(date__gte=timezone.now().date() - timezone.timedelta(days=7)).count()
       monthly_count = logs.filter(date__month=timezone.now().month).count()
       streak = logs.count()  # Replace with actual streak logic later

    reports.append({
            'habit': habit,
            'daily_count': daily_count,
            'weekly_count': weekly_count,
            'monthly_count': monthly_count,
            'streak': streak,
        })

    context = {'reports': reports}
    return render(request, 'reports.html', context)


@login_required
def achievements_view(request):
    achievements = Achievement.objects.filter(user=request.user)
    context = {'achievements': achievements}
    return render(request, 'achievements.html', context)


@login_required
def journal_view(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        mood = request.POST.get('mood', 'Neutral')

        if content:
            JournalEntry.objects.create(user=request.user, content=content, mood=mood)
            messages.success(request, "Journal entry added.")
            return redirect('journal')
        else:
            messages.error(request, "Journal entry cannot be empty.")

    context = {'entries': entries}
    return render(request, 'journal.html', context)

@login_required
def reminders_view(request):
    reminders = Reminder.objects.filter(user=request.user)
    if request.method == 'POST':
        habit_id = request.POST.get('habit')
        time = request.POST.get('time')
        message = request.POST.get('message')

        if habit_id and time:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            Reminder.objects.create(user=request.user, habit=habit, time=time, message=message)
            messages.success(request, "Reminder set successfully!")
            return redirect('reminders')

    habits = Habit.objects.filter(user=request.user)
    return render(request, 'frontend/reminders.html', {'reminders': reminders, 'habits': habits})
