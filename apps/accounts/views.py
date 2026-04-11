from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from datetime import date, timedelta
from .models import Staff


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'Admin')


def admin_required(view_func):
    """Decorator to ensure only admin users can access"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Please login.")
        if not is_admin(request.user):
            messages.error(request, 'Only administrators can access this page.')
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return wrapper


# ==================== LOGIN VIEW ====================
@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate as Staff (username)
        user = authenticate(request, username=username_or_email, password=password)

        if user:
            if user.status:
                login(request, user)
                request.session['user_type'] = 'staff'
                request.session['user_role'] = user.role
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('index')
            else:
                messages.error(request, 'Your account is inactive.')
                return redirect('login')

        # If not Staff, try as Adopter (email)
        from apps.adoptions.models import Adopter
        try:
            adopter = Adopter.objects.get(email=username_or_email)
            if adopter.check_password(password):
                request.session['adopter_id'] = adopter.adopter_id
                request.session['adopter_email'] = adopter.email
                request.session['adopter_name'] = f"{adopter.first_name} {adopter.last_name}"
                request.session['user_type'] = 'adopter'
                messages.success(request, f'Welcome back, {adopter.first_name}!')
                return redirect('adopter_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except Adopter.DoesNotExist:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'accounts/login.html')


# ==================== LOGOUT VIEW ====================
def logout_view(request):
    # Clear adopter session if exists
    if 'adopter_id' in request.session:
        del request.session['adopter_id']
        del request.session['adopter_email']
        del request.session['adopter_name']
        del request.session['user_type']
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ==================== INDEX / DASHBOARD (Role-based) ====================
@login_required
def index(request):
    """Dashboard based on user role"""
    from apps.animals.models import Pet, MedicalRecord, Vaccination
    from apps.adoptions.models import Adoption, AdoptionApplication
    from apps.fostering.models import FosterAssignment
    from apps.shelter.models import ShelterBranch

    # Common context for all users
    context = {
        'user': request.user,
        'total_pets': Pet.objects.count(),
        'available_pets': Pet.objects.filter(status='Available').count(),
        'adopted_pets': Pet.objects.filter(status='Adopted').count(),
        'total_adoptions': Adoption.objects.count(),
        'pending_applications': AdoptionApplication.objects.filter(status='Pending').count(),
        'total_fosters': FosterAssignment.objects.filter(status='Active').count(),
        'total_staff': Staff.objects.count(),
        'total_shelters': ShelterBranch.objects.count(),
        'recent_pets': Pet.objects.all().order_by('-intake_date')[:5],
    }

    # Add vet-specific data
    if request.user.role == 'Vet':
        today = date.today()
        context['pending_medical'] = MedicalRecord.objects.filter(visit_date__isnull=True).count()
        context['upcoming_vaccinations'] = Vaccination.objects.filter(
            next_due_date__gte=today,
            next_due_date__lte=today + timedelta(days=30)
        ).count()

    return render(request, 'index.html', context)


# ==================== STAFF MANAGEMENT (ADMIN ONLY) ====================
@login_required
@admin_required
def register_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif Staff.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif Staff.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            Staff.objects.create(
                username=username, email=email, first_name=first_name,
                last_name=last_name, phone=phone, role=role,
                password=make_password(password), status=True
            )
            messages.success(request, f'Staff account created for {username}!')
            return redirect('staff_list')

    return render(request, 'accounts/register.html')


@login_required
@admin_required
def staff_list(request):
    staff_members = Staff.objects.all().order_by('-date_joined')
    return render(request, 'accounts/staff_list.html', {'staff_members': staff_members})


@login_required
@admin_required
def staff_edit(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)

    if request.method == 'POST':
        staff_member.first_name = request.POST.get('first_name')
        staff_member.last_name = request.POST.get('last_name')
        staff_member.email = request.POST.get('email')
        staff_member.phone = request.POST.get('phone')
        staff_member.role = request.POST.get('role')
        staff_member.status = request.POST.get('status') == 'on'

        new_password = request.POST.get('new_password')
        if new_password and len(new_password) >= 8:
            staff_member.set_password(new_password)

        staff_member.save()
        messages.success(request, f'Staff member updated!')
        return redirect('staff_list')

    return render(request, 'accounts/staff_edit.html', {'staff': staff_member})


@login_required
@admin_required
def staff_delete(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)

    if request.method == 'POST':
        if staff_member == request.user:
            messages.error(request, 'You cannot delete your own account!')
        else:
            staff_member.delete()
            messages.success(request, 'Staff member deleted!')
        return redirect('staff_list')

    return render(request, 'accounts/staff_confirm_delete.html', {'staff': staff_member})


# ==================== PROFILE MANAGEMENT (ALL STAFF) ====================
@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')

    return render(request, 'accounts/profile_edit.html', {'user': request.user})


@login_required
def change_password(request):
    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if not request.user.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new != confirm:
            messages.error(request, 'Passwords do not match.')
        elif len(new) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new)
            request.user.save()
            messages.success(request, 'Password changed! Please login again.')
            return redirect('login')

    return render(request, 'accounts/change_password.html')