from django.contrib import admin
from .models import Student, ActionLog

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','roll_number','class_name','email')

@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','user','action','student')
    list_filter  = ('action','user')
    date_hierarchy = 'timestamp'
