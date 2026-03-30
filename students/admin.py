from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'course', 'phone', 'fees', 'fees_paid', 'enrolled_on', 'is_active']
    list_filter   = ['course', 'is_active']
    search_fields = ['name', 'phone', 'email']
