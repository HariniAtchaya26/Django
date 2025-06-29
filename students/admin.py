from django.contrib import admin
from .models import Student, Profile, Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    # Only allow one Settings instance and prevent deletion
    def has_add_permission(self, request):
        return not Settings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Student)
admin.site.register(Profile)
