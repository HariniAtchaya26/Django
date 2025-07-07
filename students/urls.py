from django.urls import path
from .views import CustomLoginView
from django.contrib.auth.views import LoginView

from .views import StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView, ActionLogListView

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list'),  # ✅ This is the key line
    path('add/', StudentCreateView.as_view(), name='student_add'),
    path('edit/<int:pk>/', StudentUpdateView.as_view(), name='student_edit'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('logs/', ActionLogListView.as_view(), name='action_logs'),
    path('login/', CustomLoginView.as_view(), name='login'),
     path('api/login/', LoginView.as_view(), name='api-login')
]
