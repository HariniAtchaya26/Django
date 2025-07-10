from rest_framework import serializers
from .models import Student, Attendance, LeaveRequest, Mark


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


# ✅ New: Mark Serializer
class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = Mark
        fields = ['id', 'student', 'student_name', 'subject', 'semester', 'score']


# ✅ Optional: For analytics responses (read-only)
class TopperSerializer(serializers.Serializer):
    student_name = serializers.CharField()
    subject = serializers.CharField()
    semester = serializers.IntegerField()
    score = serializers.FloatField()


class OverallTopperSerializer(serializers.Serializer):
    student_name = serializers.CharField()
    total_score = serializers.FloatField()


class GenderTopperSerializer(serializers.Serializer):
    gender = serializers.CharField()
    student_name = serializers.CharField()
    total_score = serializers.FloatField()
