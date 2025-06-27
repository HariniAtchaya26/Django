from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Student

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'class_name', 'email']
    search_fields = ['name', 'roll_number', 'email']