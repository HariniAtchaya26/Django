# api/views.py

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from students.models import Student, Attendance
from .models import Teacher
from .serializers import (
    StudentSerializer,
    AttendanceSerializer,
    TeacherRegisterSerializer
)

# --------------------------
# ViewSets for Browsable API
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
# Teacher Registration (JWT)
# --------------------------

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "Teacher registered successfully."}, status=201)

# --------------------------
# Teacher Login (JWT)
# --------------------------

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
# --------------------------
# Teacher Logout
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
