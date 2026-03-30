from django.urls import path
from . import views

urlpatterns = [
    path('mark/',                    views.mark_attendance,    name='mark_attendance'),
    path('view/',                    views.attendance_view,    name='attendance_today'),
    path('view/<str:date>/',         views.attendance_view,    name='attendance_view'),
    path('history/',                 views.attendance_history, name='attendance_history'),
    path('export/',                  views.export_attendance_csv, name='export_attendance'),
]
