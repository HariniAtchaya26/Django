# students/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.mail import send_mail
from django.conf import settings

from .models import Student, ActionLog
from .forms import StudentForm  
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

# ✅ Custom Login View
class CustomLoginView(LoginView):
    template_name = 'students/login.html'
    authentication_form = AuthenticationForm

# ✅ Mixin to restrict to staff (admin)
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# ✅ List all students
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

# ✅ Create student (admin only)
class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        ActionLog.objects.create(
            user=self.request.user,
            student=self.object,
            action='create'
        )
        send_mail(
            'New student added',
            f'{self.object} was added by {self.request.user.username}.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True
        )
        messages.success(self.request, "Student created & admin notified.")
        return resp

# ✅ Update student (admin only)
class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        ActionLog.objects.create(
            user=self.request.user,
            student=self.object,
            action='update'
        )
        messages.success(self.request, "Student updated.")
        return resp

# ✅ Delete student (admin only)
class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            student=obj,
            action='delete'
        )
        messages.success(request, "Student deleted.")
        return super().delete(request, *args, **kwargs)

# ✅ Show action logs (admin only)
class ActionLogListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ActionLog
    template_name = 'students/action_logs.html'
    context_object_name = 'logs'

# ✅ Student detail view
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"
