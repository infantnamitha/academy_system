# 🎓 EduTrack — Academy Management System

A complete, beginner-friendly web application for managing a coaching center / academy.
Built with **Django + SQLite** (no external database needed).

---

## ✨ Features

| Feature | Details |
|---|---|
| **Student Management** | Add, edit, delete, view students with fees tracking |
| **Attendance System** | Mark daily attendance (Present/Absent), notes support |
| **Dashboard** | Live stats, donut chart, course breakdown |
| **Export** | Download students & attendance as CSV |
| **Admin Login** | Secure login system for academy admin |
| **Mobile Responsive** | Works on phones, tablets, and desktops |

---

## 🏗️ Project Structure

```
academy/
├── academy_project/         ← Django project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── students/                ← Student management app
│   ├── models.py            ← Student database model
│   ├── views.py             ← Add/Edit/Delete/List/Export
│   ├── forms.py             ← Form validation
│   ├── urls.py
│   └── admin.py
│
├── attendance/              ← Attendance tracking app
│   ├── models.py            ← Attendance records
│   ├── views.py             ← Mark/View/Export attendance
│   ├── urls.py
│   └── admin.py
│
├── templates/               ← HTML templates
│   ├── base.html            ← Sidebar layout (shared)
│   ├── login.html
│   ├── dashboard/
│   │   └── index.html
│   ├── students/
│   │   ├── list.html
│   │   ├── form.html        ← Add & Edit (shared)
│   │   ├── detail.html
│   │   └── confirm_delete.html
│   └── attendance/
│       ├── mark.html
│       ├── view.html
│       └── history.html
│
├── static/
│   ├── css/style.css        ← Complete design system
│   └── js/main.js           ← Sidebar, animations, helpers
│
├── manage.py
├── requirements.txt
├── setup.py                 ← One-click setup script
└── README.md
```

---

## 🚀 Quick Start (3 Steps)

### Prerequisites
- Python 3.8 or higher installed
- Terminal / Command Prompt

### Step 1 — Download & Extract
```bash
# Unzip the project and navigate into it
cd academy
```

### Step 2 — Run Setup (installs everything automatically)
```bash
python setup.py
```
This will:
- Install Django and dependencies
- Create the SQLite database
- Run all migrations
- Create the admin account (`admin` / `admin123`)

### Step 3 — Start the Server
```bash
python manage.py runserver
```

Open your browser: **http://127.0.0.1:8000**

Login with:
- **Username:** `admin`
- **Password:** `admin123`

---

## 🔧 Manual Setup (if setup.py doesn't work)

```bash
# Install dependencies
pip install -r requirements.txt

# Create database tables
python manage.py makemigrations students
python manage.py makemigrations attendance
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## 📱 Pages & URLs

| URL | Page |
|---|---|
| `/` | Dashboard |
| `/students/` | Student list |
| `/students/add/` | Add new student |
| `/students/1/` | Student profile |
| `/students/1/edit/` | Edit student |
| `/students/export/csv/` | Download student CSV |
| `/attendance/mark/` | Mark today's attendance |
| `/attendance/view/` | View today's attendance |
| `/attendance/view/2024-01-15/` | View specific date |
| `/attendance/history/` | All attendance dates |
| `/attendance/export/?date=2024-01-15` | Export attendance CSV |
| `/admin/` | Django admin panel |

---

## 🛠️ Tech Stack

- **Backend:** Python 3 + Django 4.2
- **Database:** SQLite (file-based, zero setup)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Fonts:** Sora + JetBrains Mono (Google Fonts)
- **No external JS framework needed**

---

## 🔐 Security Notes for Production

Before deploying to a live server:
1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Add your domain to `ALLOWED_HOSTS`
4. Use PostgreSQL instead of SQLite
5. Set up proper HTTPS

---

## 📊 Database Models

**Student**
```
name, phone, email, course, fees, fees_paid, enrolled_on, is_active
```

**Attendance**
```
student (FK), date, status (Present/Absent), note, marked_at
```

---

## 💡 Extending the Project

- **SMS Notifications:** Integrate Twilio for absent alerts
- **Fee Reminders:** Add celery tasks for automated reminders
- **Multiple Batches:** Add a Batch model to group students
- **Reports:** Add monthly PDF reports with ReportLab
- **REST API:** Add Django REST Framework for a mobile app
