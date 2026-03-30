"""
Students App - Models
Defines the Student database table
"""
from django.db import models

class Course(models.TextChoices):
    """Available courses at the academy"""
    MATHEMATICS   = 'Mathematics',  'Mathematics'
    SCIENCE       = 'Science',      'Science'
    ENGLISH       = 'English',      'English'
    COMPUTER      = 'Computer',     'Computer Science'
    PHYSICS       = 'Physics',      'Physics'
    CHEMISTRY     = 'Chemistry',    'Chemistry'
    BIOLOGY       = 'Biology',      'Biology'
    COMMERCE      = 'Commerce',     'Commerce'
    OTHER         = 'Other',        'Other'


class Student(models.Model):
    """Student model — one row per enrolled student"""
    name        = models.CharField(max_length=100)
    phone       = models.CharField(max_length=15)
    email       = models.EmailField(blank=True, null=True)
    course      = models.CharField(max_length=50, choices=Course.choices)
    fees        = models.DecimalField(max_digits=8, decimal_places=2)
    fees_paid   = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    enrolled_on = models.DateField(auto_now_add=True)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['-enrolled_on']

    def __str__(self):
        return f"{self.name} ({self.course})"

    @property
    def fees_due(self):
        return self.fees - self.fees_paid

    @property
    def attendance_percentage(self):
        """Calculate attendance % for this student"""
        from attendance.models import Attendance
        total = Attendance.objects.filter(student=self).count()
        if total == 0:
            return 0
        present = Attendance.objects.filter(student=self, status='Present').count()
        return round((present / total) * 100, 1)
