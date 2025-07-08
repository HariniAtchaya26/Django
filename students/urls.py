# students/urls.py

from django.urls import path
from .views import (
    StudentListCreateAPIView,
    StudentProfileUpdateAPIView,
    AttendanceCreateAPIView,
    LeaveRequestCreateAPIView,
    LeaveRequestListAPIView
)

urlpatterns = [
    path('students/', StudentListCreateAPIView.as_view(), name='student-list'),
    path('students/<int:pk>/update/', StudentProfileUpdateAPIView.as_view(), name='student-update'),
    path('attendance/add/', AttendanceCreateAPIView.as_view(), name='add-attendance'),
    path('leave/apply/', LeaveRequestCreateAPIView.as_view(), name='apply-leave'),
    path('leave/list/', LeaveRequestListAPIView.as_view(), name='list-leave'),
]
