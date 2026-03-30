#!/usr/bin/env python3
"""
EduTrack Academy — One-click Setup Script
Run this once after cloning the project:
    python setup.py
"""
import os
import sys
import subprocess

def run(cmd, **kwargs):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True, **kwargs)
    if result.returncode != 0:
        print(f"  ❌ Command failed. Check the error above.")
        sys.exit(1)

print("\n" + "="*52)
print("  EduTrack Academy — Setup")
print("="*52)

# 1. Install dependencies
print("\n📦 Installing dependencies...")
run("pip install -r requirements.txt --break-system-packages -q", cwd=os.path.dirname(__file__))

# 2. Run migrations
print("\n🗄️  Setting up database...")
run(f"{sys.executable} manage.py makemigrations students", cwd=os.path.dirname(__file__))
run(f"{sys.executable} manage.py makemigrations attendance", cwd=os.path.dirname(__file__))
run(f"{sys.executable} manage.py migrate", cwd=os.path.dirname(__file__))

# 3. Create superuser
print("\n👤 Creating admin user (admin / admin123)...")
run(
    f'{sys.executable} manage.py shell -c "'
    'from django.contrib.auth.models import User; '
    'User.objects.filter(username=\'admin\').exists() or '
    'User.objects.create_superuser(\'admin\', \'admin@academy.com\', \'admin123\')'
    '"',
    cwd=os.path.dirname(__file__)
)

print("\n✅ Setup complete!")
print("\n🚀 Start the server:")
print("   python manage.py runserver")
print("\n🌐 Open in browser:")
print("   http://127.0.0.1:8000")
print("\n🔐 Login credentials:")
print("   Username: admin")
print("   Password: admin123")
print("\n" + "="*52 + "\n")
