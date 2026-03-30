"""
Attendance App - Views
Mark attendance, view history, export to CSV
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from students.models import Student
from .models import Attendance
import csv


@login_required
def mark_attendance(request):
    """Mark attendance for all students for a given date"""
    today = timezone.localdate()
    selected_date = request.GET.get('date', str(today))

    try:
        from datetime import date
        selected_date = date.fromisoformat(selected_date)
    except ValueError:
        selected_date = today

    students = Student.objects.filter(is_active=True)

    # Get existing attendance records for this date
    existing = {
        a.student_id: a
        for a in Attendance.objects.filter(date=selected_date)
    }

    if request.method == 'POST':
        saved = 0
        for student in students:
            status = request.POST.get(f'status_{student.pk}', 'Absent')
            note   = request.POST.get(f'note_{student.pk}', '')

            # Create or update attendance record
            obj, created = Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status, 'note': note}
            )
            saved += 1

        messages.success(request, f'✅ Attendance saved for {saved} students on {selected_date}.')
        return redirect('attendance_view', date=str(selected_date))

    # Build list combining students + their existing record for this date
    student_data = []
    for s in students:
        record = existing.get(s.pk)
        student_data.append({
            'student': s,
            'record': record,
            'status': record.status if record else None,
            'note':   record.note   if record else '',
        })

    context = {
        'student_data': student_data,
        'selected_date': selected_date,
        'today': today,
        'already_marked': len(existing) > 0,
        'present_count': sum(1 for r in existing.values() if r.status == 'Present'),
        'absent_count':  sum(1 for r in existing.values() if r.status == 'Absent'),
    }
    return render(request, 'attendance/mark.html', context)


@login_required
def attendance_view(request, date=None):
    """View attendance records for a specific date"""
    from datetime import date as date_type
    today = timezone.localdate()

    if date:
        try:
            view_date = date_type.fromisoformat(str(date))
        except ValueError:
            view_date = today
    else:
        view_date = today

    records = Attendance.objects.filter(date=view_date).select_related('student')
    present = records.filter(status='Present')
    absent  = records.filter(status='Absent')

    context = {
        'records': records,
        'present': present,
        'absent': absent,
        'view_date': view_date,
        'today': today,
        'total': records.count(),
        'present_count': present.count(),
        'absent_count': absent.count(),
    }
    return render(request, 'attendance/view.html', context)


@login_required
def attendance_history(request):
    """Full attendance history with date navigation"""
    from datetime import date as date_type
    # Get all dates that have attendance records
    dates = Attendance.objects.dates('date', 'day', order='DESC')

    context = {
        'dates': dates,
    }
    return render(request, 'attendance/history.html', context)


@login_required
def export_attendance_csv(request):
    """Export attendance for a given date to CSV"""
    from datetime import date as date_type
    date_str   = request.GET.get('date', str(timezone.localdate()))
    try:
        export_date = date_type.fromisoformat(date_str)
    except ValueError:
        export_date = timezone.localdate()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{export_date}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Course', 'Phone', 'Date', 'Status', 'Note'])

    records = Attendance.objects.filter(date=export_date).select_related('student')
    for r in records:
        writer.writerow([r.student.name, r.student.course, r.student.phone, r.date, r.status, r.note])

    return response
