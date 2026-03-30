"""
Students App - Views
All CRUD operations for student management
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import Student, Course
from .forms import StudentForm
import csv


@login_required
def dashboard(request):
    """Main dashboard — shows summary stats"""
    from attendance.models import Attendance
    from django.utils import timezone

    today = timezone.localdate()
    total_students = Student.objects.filter(is_active=True).count()

    # Today's attendance summary
    today_records = Attendance.objects.filter(date=today)
    today_present = today_records.filter(status='Present').count()
    today_absent  = today_records.filter(status='Absent').count()
    today_marked  = today_records.count()

    # Course breakdown
    courses = {}
    for s in Student.objects.filter(is_active=True):
        courses[s.course] = courses.get(s.course, 0) + 1

    # Recent students
    recent_students = Student.objects.filter(is_active=True)[:5]

    context = {
        'total_students': total_students,
        'today_present': today_present,
        'today_absent': today_absent,
        'today_marked': today_marked,
        'today_not_marked': total_students - today_marked,
        'courses': courses,
        'recent_students': recent_students,
        'today': today,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def student_list(request):
    """List all students with search & filter"""
    query  = request.GET.get('q', '')
    course = request.GET.get('course', '')

    students = Student.objects.filter(is_active=True)

    if query:
        students = students.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )
    if course:
        students = students.filter(course=course)

    context = {
        'students': students,
        'courses': Course.choices,
        'query': query,
        'selected_course': course,
    }
    return render(request, 'students/list.html', context)


@login_required
def student_add(request):
    """Add a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'✅ Student "{student.name}" added successfully!')
            return redirect('student_list')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = StudentForm()

    return render(request, 'students/form.html', {'form': form, 'action': 'Add'})


@login_required
def student_edit(request, pk):
    """Edit an existing student"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Student "{student.name}" updated!')
            return redirect('student_list')
        else:
            messages.error(request, '❌ Please fix the errors below.')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/form.html', {'form': form, 'action': 'Edit', 'student': student})


@login_required
def student_delete(request, pk):
    """Soft-delete a student (mark inactive)"""
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, f'🗑️ Student "{student.name}" removed.')
        return redirect('student_list')

    return render(request, 'students/confirm_delete.html', {'student': student})


@login_required
def student_detail(request, pk):
    """Student profile with attendance history"""
    from attendance.models import Attendance
    student = get_object_or_404(Student, pk=pk)
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')

    context = {
        'student': student,
        'attendance_records': attendance_records,
        'total': attendance_records.count(),
        'present': attendance_records.filter(status='Present').count(),
        'absent': attendance_records.filter(status='Absent').count(),
    }
    return render(request, 'students/detail.html', context)


@login_required
def export_students_csv(request):
    """Export student list to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Email', 'Course', 'Fees', 'Fees Paid', 'Fees Due', 'Enrolled On', 'Attendance %'])

    for s in Student.objects.filter(is_active=True):
        writer.writerow([
            s.name, s.phone, s.email or '', s.course,
            s.fees, s.fees_paid, s.fees_due,
            s.enrolled_on, s.attendance_percentage
        ])

    return response
