from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student, Attendance,LeaveRequest, Mark
from .models import Teacher, Mark


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    date = serializers.DateField(input_formats=['%Y-%m-%d', '%d-%m-%Y'])  # Flexible formats

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status']


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


class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'student', 'student_name', 'semester', 'subject', 'marks']
class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'
