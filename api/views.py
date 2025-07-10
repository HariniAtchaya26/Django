from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Avg

from students.models import Student, Attendance, LeaveRequest
from .models import Teacher
from .models import Mark 
from .serializers import (
    StudentSerializer,
    AttendanceSerializer,
    LeaveRequestSerializer,
    MarkSerializer,
    TeacherRegisterSerializer,
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
    permission_classes = [AllowAny]

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
# Student CRUD (Function-Based)
# --------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_students(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_leave(request):
    leave_requests = LeaveRequest.objects.all()
    serializer = LeaveRequestSerializer(leave_requests, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def update_student_marks(request):
    serializer = MarkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subject_topper(request):
    # Get all subjects
    subjects = Mark.objects.values_list('subject', flat=True).distinct()
    toppers = []

    for subject in subjects:
        top_mark = Mark.objects.filter(subject=subject).order_by('-marks').first()
        if top_mark:
            toppers.append({
                'subject': subject,
                'student': top_mark.student.name,
                'marks': top_mark.marks,
            })

    return Response({'toppers': toppers})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overall_topper(request):
    students = Mark.objects.values('student').annotate(total_marks=Sum('marks')).order_by('-total_marks')
    if students:
        top = students[0]
        student_name = Student.objects.get(id=top['student']).name
        return Response({
            'student': student_name,
            'total_marks': top['total_marks']
        })
    return Response({'message': 'No data found'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gender_wise_toppers(request):
    genders = Student.objects.values_list('gender', flat=True).distinct()
    result = []

    for gender in genders:
        top_student = (
            Mark.objects
            .filter(student__gender=gender)
            .values('student')
            .annotate(total=Sum('marks'))
            .order_by('-total')
            .first()
        )
        if top_student:
            student = Student.objects.get(id=top_student['student'])
            result.append({
                'gender': gender,
                'student': student.name,
                'total_marks': top_student['total']
            })

    return Response({'gender_wise_toppers': result})

@api_view(['POST'])  # ✅ Only POST
@permission_classes([IsAuthenticated])
def add_marks(request):
    serializer = MarkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# --------------------------
# Marks and Analytics APIs
# --------------------------
class MarkCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class MarkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]

class MarkUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]

class SubjectTopperAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subject = request.GET.get('subject')
        if not subject:
            return Response({'error': 'Subject query param required'}, status=400)

        top_mark = Mark.objects.filter(subject=subject).order_by('-marks').first()
        if top_mark:
            return Response({
                'student': top_mark.student.name,
                'marks': top_mark.marks,
                'subject': subject,
                'semester': top_mark.semester
            })
        return Response({'message': 'No records found'}, status=404)

class OverallTopperAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top_student = None
        top_avg = -1
        for student in Student.objects.all():
            avg = Mark.objects.filter(student=student).aggregate(avg=Avg('marks'))['avg']
            if avg and avg > top_avg:
                top_avg = avg
                top_student = student

        if top_student:
            return Response({
                'student': top_student.name,
                'average_marks': round(top_avg, 2)
            })
        return Response({'message': 'No records found'}, status=404)

class GenderWiseTopperAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(Student, 'gender'):
            return Response({'error': 'Add gender field to Student model first'}, status=400)

        toppers = {}
        for gender in ['Male', 'Female']:
            top_student = None
            top_avg = -1
            for student in Student.objects.filter(gender=gender):
                avg = Mark.objects.filter(student=student).aggregate(avg=Avg('marks'))['avg']
                if avg and avg > top_avg:
                    top_avg = avg
                    top_student = student

            if top_student:
                toppers[gender] = {
                    'student': top_student.name,
                    'average_marks': round(top_avg, 2)
                }

        return Response(toppers)
class AddMarkAPIView(generics.CreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer