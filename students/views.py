from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Student
from django.db.models import Count

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.allowed_roles).exists()

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/list.html'
    context_object_name = 'students'

class StudentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Student
    fields = ['name', 'age', 'classroom']
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:list')
    allowed_roles = ['admin']

class StudentUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Student
    fields = ['name', 'age', 'classroom']
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:list')
    allowed_roles = ['admin']

class StudentDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('students:list')
    allowed_roles = ['admin']

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_counts'] = Student.objects.values('classroom').annotate(total=Count('id'))
        return context