from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class RoleRequiredMixin(UserPassesTestMixin):
    required_groups = []

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.required_groups).exists()

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('student-list')