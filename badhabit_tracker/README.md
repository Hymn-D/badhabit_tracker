# Bad Habit Tracker API

## Project Description

The **Bad Habit Tracker API** is a Django REST Framework–based backend system that helps users identify, track, and replace bad habits.  
It allows users to log their habits, monitor frequency and progress, create replacement plans, earn achievements, share progress, and view analytical reports over time.

This project is part of a multi-week development plan:
- **Week 1:** Core setup, authentication, habit models  
- **Week 2:** Logging system & replacement plans  
- **Week 3:** Reports, dashboard, achievements, and social activity sharing  

---

## Features

### Core Functionality
- User registration, login, and logout (JWT Authentication)
- Create, update, and delete personal habits
- Categorize habits (health, finance, productivity, etc.)
- View all habits belonging to the authenticated user

### Habit Tracking
- Log daily, weekly, or monthly occurrences
- Automatically compute progress frequency and streaks
- View analytics per habit or all habits combined

### Replacement Plans
- Suggest or create positive replacement activities
- Manage and update plans to help reduce bad habits

### Reminders & Journals
- Create reminders for habits with motivational messages
- Write journal entries reflecting on mood and triggers

### Achievements & Dashboard
- Automatically award achievements for consistency
- View detailed reports on habit performance and history
- Dashboard summary for all progress metrics

### Social & Leaderboards
- Share achievements or progress with other users or social platforms
- View leaderboards of top users by streaks or logged activities

---

##  Technologies Used

| Technology | Purpose |
|-------------|----------|
| **Django** | Backend framework for building scalable web applications |
| **Django REST Framework (DRF)** | Simplifies creation of RESTful APIs |
| **SimpleJWT** | Secure authentication with JSON Web Tokens |
| **SQLite/PostgreSQL** | Database for storing user and habit data |
| **Python 3.12+** | Primary language used for development |
| **VS Code** | Development environment |

---

## Why These Technologies

- **Django** provides robust ORM, admin interface, and scalability.  
- **DRF** simplifies API serialization and permission handling.  
- **JWT Authentication** ensures stateless, secure user sessions.  
- **PostgreSQL** (or SQLite for dev) offers reliability and ACID compliance.  
- **Python** allows quick development and clean, maintainable code.

---

## How to Use the Project

## Authentication
Register: POST /api/auth/register/
Login: POST /api/auth/login/
Logout: POST /api/auth/logout/

---

## Habits

List Habits: GET /api/habits/
Create Habit: POST /api/habits/
Update Habit: PUT /api/habits/{id}/
Delete Habit: DELETE /api/habits/{id}/

---

## Logs

Add Log: POST /api/habits/{habit_id}/logs/
View Logs: GET /api/habits/{habit_id}/logs/
Replacement Plans
List Plans: GET /api/habits/{habit_id}/plans/
Create Plan: POST /api/habits/{habit_id}/plans/

---

## Reports & Dashboard

Summary: GET /api/reports/summary/
Detailed Habit Report: GET /api/reports/habits/{habit_id}/
Achievements: GET /api/achievements/
Leaderboard: GET /api/leaderboard/
Share Activity: POST /api/share/
All endpoints require authentication using JWT tokens.

---

Author

[Esther]
Django Developer | Habit Tracking Enthusiast
📧 ogbonnajunia12@gmail.com
🌐(https://github.com/Hymn-D)