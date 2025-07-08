# students/views.py

from rest_framework import generics, permissions
from .models import Student, Attendance, LeaveRequest
from .serializer import StudentSerializer, AttendanceSerializer, LeaveRequestSerializer

class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class AttendanceCreateAPIView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveRequestCreateAPIView(generics.CreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveRequestListAPIView(generics.ListAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
