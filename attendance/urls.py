from django.urls import path
from . import views 
from .views import MarkAttendanceView, AttendanceExportCSV

urlpatterns = [
    path('mark/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('export/', AttendanceExportCSV.as_view(), name='export_attendance'),
    # attendance/urls.py
    path('export/', views.export_attendance_csv, name='export_attendance_csv'),

]
