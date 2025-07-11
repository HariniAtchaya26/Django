from django.db import models
from django.contrib.auth.models import User

# --- Student & Related Models ---
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    student_class = models.CharField(max_length=20)
    age = models.IntegerField()
    profile_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    document = models.FileField(upload_to='student_docs/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='legacy_attendance')
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
    student = models.ForeignKey(Student, null=True, blank=True, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action}"

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=50)
    semester = models.IntegerField()
    score = models.FloatField()

    class Meta:
        unique_together = ['student', 'subject', 'semester']

    def __str__(self):
        return f"{self.student.name} - {self.subject} - Sem {self.semester} - {self.score}"

# --- Class, Subjects, Teacher Models ---
class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, through='TeacherSubject')  # ✅ Insert here

    def __str__(self):
        return self.user.username

class TeacherSubject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher} teaches {self.subject}"


# --- Timetable Models ---
WEEKDAYS = (
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
)

class Period(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

class Timetable(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)

    class Meta:
        unique_together = ('student_class', 'period', 'weekday')

    def __str__(self):
        return f"{self.student_class.name} | {self.weekday} | {self.period}"
