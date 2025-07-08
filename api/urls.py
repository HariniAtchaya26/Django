from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, StudentViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # ✅ Add this
    path('', include(router.urls)),
]
