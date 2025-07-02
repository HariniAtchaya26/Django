from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    def get_absolute_url(self):
        return reverse('student_list')

class ActionLog(models.Model):
    ACTION_CHOICES = (
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    )
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    action     = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} {self.student} at {self.timestamp}"
