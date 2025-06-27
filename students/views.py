from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistrationForm


from .models import Student
from .forms import StudentForm

# Role checkers
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_viewer(user):
    return user.groups.filter(name='Viewer').exists()

def is_admin_or_viewer(user):
    return is_admin(user) or is_viewer(user)

# Register view
def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        messages.success(request, "Registration successful! Ask admin to assign your role.")
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})

# Login view
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('student_list')
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Student list view
@login_required
@user_passes_test(is_admin_or_viewer)
def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

# Add student (admin only)
@login_required
@user_passes_test(is_admin)
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect('student_list')
    return render(request, 'students/add.html', {'form': form})

# Edit student (admin only)
@login_required
@user_passes_test(is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully.")
        return redirect('student_list')
    return render(request, 'students/edit.html', {'form': form})              
def register_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})