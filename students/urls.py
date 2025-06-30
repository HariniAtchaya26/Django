from django.urls import path
from .views import SettingsView, export_students_csv
from .views import (
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
    DashboardView,
    SettingsView,
    export_students_csv,
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('add/', StudentCreateView.as_view(), name='student_add'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('export-csv/', export_students_csv, name='export_students_csv'),
    
]
