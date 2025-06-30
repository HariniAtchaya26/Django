import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models import Q

from attendance.models import Attendance
from .models import Student, Settings
from .forms import SettingsForm
from .mixins import AdminRequiredMixin


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['settings_obj'] = Settings.objects.first()
        return ctx


class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Student
    fields = ['name', 'roll_number', 'class_name', 'email']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        settings = Settings.objects.first()
        count = Student.objects.filter(class_name=form.instance.class_name).count()
        if settings and count > settings.max_students_per_class:
            messages.warning(
                self.request,
                f"Class {form.instance.class_name} now has {count} students "
                f"(exceeds max of {settings.max_students_per_class})."
            )
        return response


class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Student
    fields = ['name', 'roll_number', 'class_name', 'email']
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        settings = Settings.objects.first()
        count = Student.objects.filter(class_name=form.instance.class_name).count()
        if settings and count > settings.max_students_per_class:
            messages.warning(
                self.request,
                f"Class {form.instance.class_name} now has {count} students "
                f"(exceeds max of {settings.max_students_per_class})."
            )
        return response


class StudentDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['class_counts'] = Student.objects.values('class_name').annotate(count=Count('id'))

        attendance_stats = []
        for student in Student.objects.all():
            total = Attendance.objects.filter(student=student).count()
            present = Attendance.objects.filter(student=student, status='present').count()
            percent = (present / total * 100) if total > 0 else 0

            attendance_stats.append({
                'student': student,
                'present': present,
                'total': total,
                'percent': round(percent, 2),
            })

        ctx['attendance_stats'] = attendance_stats
        return ctx


class SettingsView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'students/settings.html'

    def get(self, request):
        settings_obj, _ = Settings.objects.get_or_create(pk=1)
        form = SettingsForm(instance=settings_obj)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        settings_obj, _ = Settings.objects.get_or_create(pk=1)
        form = SettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('settings')
        return render(request, self.template_name, {'form': form})


def export_students_csv(request):
    try:
        user_role = request.user.profile.role
    except Exception:
        messages.error(request, "User profile is missing. Please contact admin.")
        return redirect('student_list')

    settings_obj = Settings.objects.first()
    if not settings_obj or (
        user_role != 'admin' and not settings_obj.allow_viewer_download
    ):
        messages.error(request, "You’re not allowed to download the student list.")
        return redirect('student_list')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Roll Number', 'Class', 'Email'])

    for s in Student.objects.all():
        writer.writerow([s.name, s.roll_number, s.class_name, s.email])

    return response
