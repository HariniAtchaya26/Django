from django.shortcuts       import render, redirect
from django.urls           import reverse_lazy
from django.contrib        import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic  import ListView, CreateView, UpdateView, DeleteView
from django.core.mail      import send_mail
from django.conf           import settings
from django.views.generic import ListView
from .models import Student


from .models    import Student, ActionLog
from .forms     import StudentForm

# ensures only staff can add/edit/delete
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        # log
        ActionLog.objects.create(
            user=self.request.user,
            student=self.object,
            action='create'
        )
        # email admin
        send_mail(
            'New student added',
            f'{self.object} was added by {self.request.user.username}.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True
        )
        messages.success(self.request, "Student created & admin notified.")
        return resp

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

class ActionLogListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ActionLog
    template_name = 'students/action_logs.html'
    context_object_name = 'logs'
from django.views.generic.detail import DetailView
from .models import Student

class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"  # You can create this HTML file
class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'  # ✅ Path to your template
    context_object_name = 'students'

from django.views.generic import ListView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'    