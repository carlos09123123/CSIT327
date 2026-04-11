from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def staff_required(view_func):
    """Decorator to check if user is staff (not an adopter)"""
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated via Django (Staff)
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        # Check if it's an adopter session
        elif 'adopter_id' in request.session:
            raise PermissionDenied("You don't have permission to access this page.")
        else:
            raise PermissionDenied("Please login to continue.")
    return wrapper

def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Admin':
            return view_func(request, *args, **kwargs)
        elif 'adopter_id' in request.session:
            raise PermissionDenied("Adopters cannot access staff pages.")
        else:
            raise PermissionDenied("You don't have permission to access this page.")
    return wrapper