from django.contrib import admin
from .models import Student, Attendance, ActionLog  # ✅ Make sure ActionLog is imported

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'student_class')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'action', 'timestamp']
