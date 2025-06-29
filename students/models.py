from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Student model
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

# Profile model
class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('viewer', 'Viewer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Settings model
class Settings(models.Model):
    max_students_per_class = models.PositiveIntegerField(default=30)
    allow_viewer_download = models.BooleanField(default=False)

    def clean(self):
        # Only one Settings instance allowed
        if Settings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one Settings instance allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

# ✅ Signal to auto-create or update Profile for User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
