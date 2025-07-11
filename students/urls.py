from django.urls import path
from .views import add_marks
from .views import teacher_timetable_view, student_timetable_view
from .views import (
    StudentListCreateAPIView,
    StudentProfileUpdateAPIView,
    AttendanceCreateAPIView,
    LeaveRequestCreateAPIView,
    LeaveRequestListAPIView,
    MarkListCreateAPIView,
    MarkUpdateAPIView,
    SubjectWiseTopperAPIView,
    OverallTopperAPIView,
    GenderWiseTopperAPIView,
    
)

urlpatterns = [
    # ----- Student -----
    path('students/', StudentListCreateAPIView.as_view(), name='student-list'),
    path('students/<int:pk>/update/', StudentProfileUpdateAPIView.as_view(), name='student-update'),

    # ----- Attendance -----
    path('attendance/add/', AttendanceCreateAPIView.as_view(), name='add-attendance'),
     path('marks/add/', add_marks, name='add-marks'),

    # ----- Leave -----
    path('leave/apply/', LeaveRequestCreateAPIView.as_view(), name='apply-leave'),
    path('leave/list/', LeaveRequestListAPIView.as_view(), name='list-leave'),

    # ----- ✅ Marks -----
    path('marks/', MarkListCreateAPIView.as_view(), name='mark-list-create'),
    path('marks/<int:pk>/update/', MarkUpdateAPIView.as_view(), name='mark-update'),

    # ----- ✅ Analytics -----
    path('analytics/subject-topper/', SubjectWiseTopperAPIView.as_view(), name='subject-topper'),
    path('analytics/overall-topper/', OverallTopperAPIView.as_view(), name='overall-topper'),
    path('analytics/gender-topper/', GenderWiseTopperAPIView.as_view(), name='gender-topper'),

    path('teacher/timetable/', teacher_timetable_view, name='teacher-timetable'),
    path('student/timetable/', student_timetable_view, name='student-timetable'),
]
