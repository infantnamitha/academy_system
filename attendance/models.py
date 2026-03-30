"""
Attendance App - Models
Stores daily attendance records for each student
"""
from django.db import models
from students.models import Student


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent',  'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_set')
    date    = models.DateField()
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    note    = models.CharField(max_length=200, blank=True)  # optional note (e.g., "Medical leave")
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Each student can have only ONE record per day
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__name']

    def __str__(self):
        return f"{self.student.name} — {self.date} — {self.status}"
