from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max, Sum
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from students.models import Teacher, Timetable
from students.models import Student, Timetable
from .models import Student, Attendance, LeaveRequest, Mark
from .models import Timetable, Class, Subject, Teacher, Period
from .serializer import (
    StudentSerializer,
    AttendanceSerializer,
    LeaveRequestSerializer,
    MarkSerializer,
    TopperSerializer,
    OverallTopperSerializer,
    GenderTopperSerializer
)


# ------------------------- Existing Views -------------------------

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


# ------------------------- ✅ Mark Views -------------------------

class MarkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [permissions.IsAuthenticated]


class MarkUpdateAPIView(generics.UpdateAPIView):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    permission_classes = [permissions.IsAuthenticated]


# ------------------------- ✅ Analytics Views -------------------------

class SubjectWiseTopperAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        toppers = []
        subjects = Mark.objects.values_list('subject', flat=True).distinct()
        semesters = Mark.objects.values_list('semester', flat=True).distinct()

        for subject in subjects:
            for semester in semesters:
                top_mark = Mark.objects.filter(subject=subject, semester=semester).order_by('-score').first()
                if top_mark:
                    toppers.append({
                        'student_name': top_mark.student.name,
                        'subject': subject,
                        'semester': semester,
                        'score': top_mark.score
                    })

        return Response(toppers)


class OverallTopperAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        scores = Mark.objects.values('student__name').annotate(total_score=Sum('score')).order_by('-total_score')
        if scores:
            return Response({
                'student_name': scores[0]['student__name'],
                'total_score': scores[0]['total_score']
            })
        return Response({'message': 'No data'}, status=status.HTTP_404_NOT_FOUND)


class GenderWiseTopperAPIView(APIView):
    def get(self, request):
        toppers = {}
        gender_groups = Student.objects.values('gender').distinct()

        for group in gender_groups:
            gender = group['gender']
            student = (
                Student.objects.filter(gender=gender)
                .annotate(total_score=Sum('marks__score'))
                .order_by('-total_score')
                .first()
            )
            if student:
                toppers[gender] = {
                    "student": student.name,
                    "total_score": student.total_score
                }

        return Response(toppers)
@api_view(['POST'])
def add_marks(request):
    serializer = MarkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@login_required
def teacher_timetable_view(request):
    teacher = Teacher.objects.get(user=request.user)
    schedule = Timetable.objects.filter(teacher=teacher).order_by('weekday', 'period__start_time')
    return render(request, 'students/teacher_timetable.html', {'schedule': schedule})
@login_required
def student_timetable_view(request):
    student = Student.objects.get(user=request.user)
    schedule = Timetable.objects.filter(classroom=student.student_class).order_by('weekday', 'period__start_time')
    return render(request, 'students/student_timetable.html', {'schedule': schedule})
