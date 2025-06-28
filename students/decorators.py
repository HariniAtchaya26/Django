# students/decorators.py
from django.core.exceptions import PermissionDenied

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'profile'):
                if request.user.profile.role == role:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
