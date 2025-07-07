# api/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .serializers import StudentSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from students.models import Student, Attendance
from .models import Teacher
from .serializers import (
    StudentSerializer,
    AttendanceSerializer,
    TeacherRegisterSerializer
)

# --------------------------
# DRF ViewSets for Browsable API
# --------------------------

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

# --------------------------
# Teacher Registration
# --------------------------

@api_view(['POST'])
def register_teacher(request):
    serializer = TeacherRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher registered successfully."}, status=201)
    return Response(serializer.errors, status=400)

# --------------------------
# Teacher Login (returns JWT tokens)
# --------------------------

@api_view(['POST'])
def login_teacher(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"error": "Invalid credentials"}, status=401)

# --------------------------
# Logout by blacklisting refresh token
# --------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_teacher(request):
    try:
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# --------------------------
# Add Student
# --------------------------

@api_view(['POST'])  # ✅ POST only
@permission_classes([IsAuthenticated])  # ✅ Requires token
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# --------------------------
# List Students
# --------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

# --------------------------
# Optional: Legacy JSON login for testing (not JWT)
# --------------------------


