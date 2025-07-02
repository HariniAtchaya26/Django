from django.urls import path
from .views import (
    StudentListView, StudentCreateView, StudentUpdateView,
    StudentDetailView, StudentDeleteView
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('add/', StudentCreateView.as_view(), name='student_add'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('detail/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),

]
