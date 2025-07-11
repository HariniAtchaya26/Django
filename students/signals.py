from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student, ActionLog
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Teacher
from api.models import Profile 
from students.models import Teacher
from api.models import Profile  # 

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.profile.role == 'Teacher':
                Teacher.objects.create(user=instance)
        except Profile.DoesNotExist:
            pass  # Profile hasn't been created yet

@receiver(post_save, sender=Student)
def log_student_save(sender, instance, created, **kwargs):
    request = getattr(instance, '_request', None)
    if request:
        user = request.user
        action = 'create' if created else 'update'
        ActionLog.objects.create(user=user, action=action, student=instance)

        if action == 'create':
            send_mail(
                subject="New student added",
                message=f"Student {instance.name} has been added by {user.username}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin.email for admin in User.objects.filter(is_superuser=True)],
                fail_silently=True
            )

@receiver(post_delete, sender=Student)
def log_student_delete(sender, instance, **kwargs):
    request = getattr(instance, '_request', None)
    if request:
        user = request.user
        ActionLog.objects.create(user=user, action='delete', student=instance)
