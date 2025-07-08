from django.db import models
from students.models import Student

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
    )
class Attendance(models.Model):
    student = models.ForeignKey('students.Student', null=True, blank=True, on_delete=models.CASCADE)  # ✅ FIXED
    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))


    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
