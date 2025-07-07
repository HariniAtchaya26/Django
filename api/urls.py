from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    AttendanceViewSet,
    register_teacher,
    login_teacher,
    logout_teacher,
    add_student,
    list_students,
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    # Teacher JWT auth
    path('register/', register_teacher, name='register_teacher'),
    path('login/', login_teacher, name='login_teacher'),
    path('logout/', logout_teacher, name='logout_teacher'),

    # Teacher manual student management
   path('students/add/', add_student, name='add_student'), 
    path('students/list/', list_students, name='list_students'),

    # ViewSet router URLs (CRUD for students & attendance)
    path('', include(router.urls)),
]
