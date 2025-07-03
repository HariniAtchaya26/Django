from django.db import models
from django.contrib.auth.models import User

# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

# Attendance model (linked to Student)
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

# Action Log model
class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('Added', 'Added'),
        ('Edited', 'Edited'),
        ('Deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.student} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
