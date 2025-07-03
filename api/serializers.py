from rest_framework import serializers
from students.models import Student, Attendance
from datetime import datetime


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'student_class']

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()  # shows student name

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status']
class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y'])  # 👈 Add both formats

    class Meta:
        model = Attendance
        fields = '__all__'