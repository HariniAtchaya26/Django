from django.db import models
from django.contrib.auth.models import User
from students.models import Student
ROLE_CHOICES = (
    ('Admin', 'Admin'),
    ('Viewer', 'Viewer'),
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_teacher')
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Leave'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')

    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_marks')
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.subject} ({self.semester})"
    
    