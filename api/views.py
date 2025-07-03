from rest_framework import viewsets
from students.models import Student, Attendance
from .serializers import StudentSerializer, AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
