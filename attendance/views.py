from django.shortcuts import render, redirect
from django.views import View
from .models import Attendance
from students.models import Student
from django.contrib import messages
from datetime import date
from django.http import HttpResponse
import csv

class MarkAttendanceView(View):
    def get(self, request):
        students = Student.objects.all()
        today = date.today()
        records = {att.student_id: att for att in Attendance.objects.filter(date=today)}
        return render(request, 'attendance/mark_attendance.html', {'students': students, 'records': records})

    def post(self, request):
        today = date.today()
        for key, value in request.POST.items():
            if key.startswith('status_'):
                student_id = int(key.split('_')[1])
                status = value
                Attendance.objects.update_or_create(
                    student_id=student_id,
                    date=today,
                    defaults={'status': status}
                )
        messages.success(request, "Attendance marked successfully!")
        return redirect('mark_attendance')

class AttendanceExportCSV(View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
        writer = csv.writer(response)
        writer.writerow(['Student', 'Date', 'Status'])
        for record in Attendance.objects.all():
            writer.writerow([record.student.name, record.date, record.status])
        return response
    

def export_attendance_csv(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    student_id = request.GET.get('student')

    records = Attendance.objects.all()
    if start_date and end_date:
        records = records.filter(date__range=[start_date, end_date])
    if student_id:
        records = records.filter(student_id=student_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student', 'Date', 'Status'])

    for a in records:
        writer.writerow([a.student.name, a.date, a.status])

    return response
    
