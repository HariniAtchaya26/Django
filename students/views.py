from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

from .models import Student, ActionLog
from .forms import StudentForm
from django.contrib.auth.models import User

# Utility to send email to admin
def send_admin_email_if_needed(student_name, performed_by):
    subject = f"New Student Added: {student_name}"
    message = f"{performed_by.username} added a new student named {student_name}."
    admin_emails = [user.email for user in User.objects.filter(is_superuser=True)]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ActionLogListView(ListView):
    model = ActionLog
    template_name = 'students/action_logs.html'
    context_object_name = 'logs'
    ordering = ['-timestamp']

class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send email after successful save
        send_mail(
            subject='New Student Added',
            message=f'Student "{self.object.name}" was added by {self.request.user}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['admin@example.com'],  # replace with real admin email
            fail_silently=False,
        )

        return response

    def test_func(self):
        return self.request.user.profile.role == 'Admin'

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        ActionLog.objects.create(
            user=self.request.user,
            action='EDIT',
            student_name=form.instance.name
        )
        messages.success(self.request, "Student updated successfully!")
        return response

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action='DELETE',
            student_name=student.name
        )
        messages.success(request, "Student deleted successfully!")
        return super().delete(request, *args, **kwargs)
    def role_based_login_redirect(request):
        if request.user.is_authenticated:
            if request.user.profile.role == 'Admin':
                messages.success(request, "Welcome Admin!")
            elif request.user.profile.role == 'Viewer':
                messages.info(request, "Welcome Viewer!")
        return redirect('student_list')      
        



    


