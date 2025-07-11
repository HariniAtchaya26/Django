from django.contrib import admin
from .models import Student, Attendance, ActionLog  # ✅ Make sure ActionLog is imported
from .models import Teacher, Class, Period, Timetable 
from .models import Subject # ✅ fix here: use Timetable not TimetableEntry

admin.site.register(Teacher)
admin.site.register(Class)
admin.site.register(Period)
admin.site.register(Timetable)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'student_class')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'action', 'timestamp']
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']