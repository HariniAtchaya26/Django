from rest_framework import serializers
from students.models import Student, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'student_class']

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # shows student name

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status']
