from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from .models import Student
from .forms import StudentForm

class StudentListView(ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get(self, request, *args, **kwargs):
        if request.headers.get('HX-Request'):
            self.template_name = 'students/student_list_partial.html'
        return super().get(request, *args, **kwargs)

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'

    def form_valid(self, form):
        self.object = form.save()
        students = Student.objects.all()
        return render(self.request, 'students/student_list_partial.html', {'students': students})

    def form_invalid(self, form):
        return render(self.request, 'students/student_form.html', {'form': form})

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'

    def form_valid(self, form):
        self.object = form.save()
        students = Student.objects.all()
        return render(self.request, 'students/student_list_partial.html', {'students': students})

    def form_invalid(self, form):
        return render(self.request, 'students/student_form.html', {'form': form})

class StudentDetailView(DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        students = Student.objects.all()
        return render(request, 'students/student_list_partial.html', {'students': students})
