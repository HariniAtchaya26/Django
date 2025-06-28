from django.urls import path
from .views import RegisterView
from .views import StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),
    path('add/', StudentCreateView.as_view(), name='student_add'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('register/', RegisterView.as_view(), name='register'),  # 👈 add this
]