# students/admin.py
from django.contrib import admin
from .models import Student, Profile  # ✅ Only import models that exist

admin.site.register(Student)
admin.site.register(Profile)
