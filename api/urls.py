from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import subject_topper, overall_topper, gender_wise_toppers
from .views import add_marks, AddMarkAPIView

from .views import (
    RegisterView,
    LoginView,
    logout_teacher,
    StudentViewSet,
    AttendanceViewSet,
    add_student,
    list_students,
    update_student_marks,

    MarkCreateAPIView
)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_teacher, name='logout'),

    # Students
    path('students/add/', add_student, name='add-student'),
    path('students/list/', list_students, name='list-students'),

    # Marks update + analytics
    path('students/<int:student_id>/marks/', update_student_marks, name='update-student-marks'),
   path('analytics/subject-topper/', subject_topper),
    path('analytics/overall-topper/', overall_topper),
    path('analytics/gender-wise/', gender_wise_toppers),
    path('marks/add/', MarkCreateAPIView.as_view(), name='add-marks'),
    path('marks/update/', update_student_marks, name='update-marks'),
    path('marks/add/', add_marks, name='add-marks'),
      path('marks/add/', AddMarkAPIView.as_view(), name='add-marks'),
]
