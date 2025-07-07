from rest_framework import serializers
from students.models import Student, Attendance
from datetime import datetime
from django.contrib.auth.models import User
from .models import Teacher, Student
from students.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =  ['id','student_id', 'name', 'age', 'roll_number', 'student_class']

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class TeacherRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'subject']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'        