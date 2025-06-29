# students/mixins.py

from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Allows access if user is a Django superuser or has Profile.role == 'admin'.
    """
    def test_func(self):
        user = self.request.user
        # Superusers always pass
        if user.is_superuser:
            return True
        # Otherwise must have a Profile with role='admin'
        return hasattr(user, 'profile') and user.profile.role == 'admin'
