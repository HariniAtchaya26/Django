from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        help_text="Max 30 characters. Letters, digits and @/./+/-/_ only.",
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    # You can extend later with phone, profile_pic, etc.

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name