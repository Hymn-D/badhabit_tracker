
🧠 Bad Habit Tracker
---

The **Bad Habit Tracker** is a personal productivity and wellness web app built with Django 
that helps users **identify, track, and replace bad habits** with positive alternatives.  
It allows users to log habits, reflect through journals, set reminders, monitor frequency and 
progress, create replacement plans, earn achievements, share progress, and view analytical reports 
over time, as they make progress toward a healthier lifestyle.

---

## What the Application Does
This application helps users:
-  **Register and log in** to their personal account.  
-  **Track bad habits** — record when and how often they occur.  
-  **Add replacement plans** — create positive activities to replace harmful habits.  
-  **Log daily, weekly, and monthly occurrences** of habits.  
-  **Set reminders** to stay consistent and receive motivational messages.  
-  **Journal reflections** to understand emotional triggers.  
-  **Earn achievements** and streaks for positive progress.  
-  **View detailed reports and dashboards** showing analytics over time.  
-  **Share achievements** or activity highlights on social media.

---

# Features

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
##folder structure
badhabit_tracker/
│
├── badhabit_tracker/
│   ├── settings.py
│   ├── urls.py
│
├── habits/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── frontend/
│   ├── views.py
│   ├── urls.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── habits.html
│   ├── reminders.html
│   ├── reports.html
│   ├── achievements.html
│   ├── journal.html
│   ├── login.html
│   ├── register.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│
├── manage.py
└── requirements.txt
---

## Technologies Used
- **Django** (Python) – backend web framework and ORM.  
- **Django REST Framework (DRF)** – to create API endpoints.
- **SimpleJWT** Secure authentication with JSON Web Tokens. 
- **Celery & Redis** (optional) – for background reminder notifications.  
- **HTML5, CSS3, JavaScript** – frontend for user interaction.  
- **Bootstrap** – responsive and elegant UI design.  
- **SQLite3 ** – database for storing habits and logs.  
- **JWT Authentication** – secure login and token management.  
- **python anywhere** – deployment platform for production hosting.
- **Python 3.12+** Primary language used for development.
- **VS Code** Development environment.
---

## Why These Technologies
- **Django** offers a stable, scalable, and well-documented framework ideal for rapid development.
- **DRF** simplifies API creation and integration between frontend and backend.
- **Bootstrap** and **JavaScript** enable quick, user-friendly frontend design.
- **Celery** supports scheduling reminders asynchronously.
- **PostgreSQL** ensures strong relational data integrity for complex habit tracking.
- **pythonanywhere** easy to deploy and use for projects.

---

## How to Install and Run the Project--
--Clone the Repository--
git clone https://github.com/your-username/badhabit_tracker.git
cd badhabit_tracker

--Create and Activate Virtual Environment 
python -m venv venv
venv\Scripts\activate      # on Windows
source venv/bin/activate   # on Mac/Linux

--Install Dependencies
pip install -r requirements.txt

--Run Migrations
python manage.py makemigrations
python manage.py migrate

--Create a Superuser (for admin access)
python manage.py createsuperuser

--Run the Server
python manage.py runserver
Then visit:
👉 http://127.0.0.1:8000/
---

## How to Use the Project---
--Register or Login--
Navigate to /register/ or /login/ to create an account.

--Add a Habit--
Go to /habits/ and click Add Habit.
Fill in the habit name, category, and description.

--Log a Habit--
Open any habit to record when it occurs daily, weekly, or monthly.

--Set Reminders--
Visit /reminders/ to set times and motivational messages.

--Track Progress--
View reports on /reports/ to see streaks and analytics.

--Journal & Reflect--
Write journal entries at /journal/ to document triggers and progress.

--Earn Achievements--
Achievements appear on /achievements/ as you log consistently.

--View Dashboard--
The / homepage shows an overview of your habits, logs, and reminders.

--View Dashboard--
view dashboard on dashbaord/ 
All endpoints require authentication using JWT tokens.
---

--Challenges Faced--
Integrating Celery for SMS reminders and ensuring tasks trigger correctly.
Designing database relationships for multiple related models (Habit → Log → ReplacementPlan → Reminder).
Structuring reusable templates for multiple pages while keeping consistent UI.
Managing authentication tokens between API and frontend.

--Future Improvements--
Add a mobile-friendly React or Flutter frontend.
Integrate Twilio SMS / email reminders for notifications.
Enable social sharing of achievements and leaderboard stats.
Implement AI habit suggestions based on logged data.
Add data visualization with Chart.js for reports.
---
##Author
-Esther
-Django Developer | Habit Tracking Enthusiast
-Built with ❤️ using Django and a passion for positive change.

--
## 🌍 Live Demo
You can access the deployed app here:  
👉 [https://Quebit.pythonanywhere.com](Quebit.pythonanywhere.com)
--
