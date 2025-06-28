from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class StudentForm(forms.Form):
    name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=20)
    class_name = forms.CharField(max_length=50)
    email = forms.EmailField()

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
