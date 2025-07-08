# students/models.py

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=20)
    age = models.IntegerField()
    profile_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    document = models.FileField(upload_to='student_docs/', null=True, blank=True)
 
    def __str__(self):
        return self.name

class Attendance(models.Model):

    
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='student_attendances')
    date = models.DateField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

class LeaveRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.date}"
class ActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', null=True, blank=True, on_delete=models.CASCADE)  # ✅ FIXED
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.action}"
