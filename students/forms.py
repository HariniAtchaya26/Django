from django import forms
from .models import Settings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['max_students_per_class', 'allow_viewer_download']
