from datetime import date, datetime, timedelta
from django.utils import timezone
from typing import Iterable, Set, Tuple

def today_utc_date():
    return timezone.now().date()

def start_of_week(dt: date):
    return dt - timedelta(days=dt.weekday())

def end_of_week(dt: date) -> date:
    return start_of_week(dt) + timedelta(days=6)

def start_of_month(dt: date):
    return dt.replace(day=1)


def end_of_month(dt: date) -> date:
    if dt.month == 12:
        next_month = dt.replace(year=dt.year + 1, month=1, day=1)
    else:
        next_month = dt.replace(month=dt.month + 1, day=1)
    return next_month - timedelta(days=1)

def daterange(start_date: date, end_date: date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

def compute_streaks(dates_with_logs_set, upto_date=None):
  
    if upto_date is None:
        upto_date = today_utc_date()

    current = 0
    d = upto_date
    while d in dates_with_logs_set:
        current += 1
        d = d - timedelta(days=1)

    if not dates_with_logs_set:
        return current, 0

    sorted_dates = sorted(dates_with_logs_set)
    longest = 1
    run = 1
    prev = sorted_dates[0]
    for cur in sorted_dates[1:]:
        if (cur - prev).days == 1:
            run += 1
        else:
            if run > longest:
                longest = run
            run = 1
        prev = cur
    if run > longest:
        longest = run

    return current, longest


def safe_percent_change(current: float, previous: float) -> float:
    if previous == 0:
        if current == 0:
            return 0.0
        return 100.0
    return round(((current - previous) / previous) * 100.0, 2)
