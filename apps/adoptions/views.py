from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum
from datetime import datetime
from .models import Adopter, AdoptionApplication, Interview, HomeVisit, Adoption, Payment
from .forms import AdopterRegistrationForm
from apps.animals.models import Pet


# ==================== ADOPTER REGISTRATION (PUBLIC) ====================
@csrf_protect
def adopter_register(request):
    """Public registration for adopters - anyone can access"""
    if request.method == 'POST':
        form = AdopterRegistrationForm(request.POST)
        if form.is_valid():
            adopter = form.save(commit=False)
            adopter.set_password(form.cleaned_data['password'])
            adopter.save()
            messages.success(request, 'Registration successful! You can now log in with your email.')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = AdopterRegistrationForm()

    return render(request, 'adoptions/adopter_register.html', {'form': form})


# ==================== ADOPTER DASHBOARD ====================
def adopter_dashboard(request):
    """Dashboard for adopters after login - shows available pets and their applications"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    try:
        adopter = Adopter.objects.get(adopter_id=request.session['adopter_id'])
    except Adopter.DoesNotExist:
        messages.error(request, 'Adopter not found.')
        return redirect('login')

    # Get available pets for adoption
    available_pets = Pet.objects.filter(status='Available')

    # Get adopter's applications
    applications = AdoptionApplication.objects.filter(adopter=adopter).order_by('-application_date')

    context = {
        'adopter': adopter,
        'user_name': request.session.get('user_name', f"{adopter.first_name} {adopter.last_name}"),
        'user_email': request.session.get('user_email', adopter.email),
        'session_login_time': request.session.get('login_time', 'Just now'),
        'available_pets': available_pets,
        'applications': applications,
    }
    return render(request, 'index.html', context)


# ==================== ADOPTER APPLICATION ACTIONS ====================
@csrf_protect
def adopter_apply(request, pet_id):
    """Adopter applies for a specific pet"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    adopter = get_object_or_404(Adopter, adopter_id=request.session['adopter_id'])
    pet = get_object_or_404(Pet, pet_id=pet_id)

    # Check if pet is available
    if pet.status != 'Available':
        messages.error(request, f'{pet.name} is no longer available for adoption.')
        return redirect('adopter_apply_list')

    # Check if adopter has too many pending applications (max 3)
    pending_count = AdoptionApplication.objects.filter(adopter=adopter, status='Pending').count()
    if pending_count >= 3:
        messages.error(request, 'You already have 3 pending applications. Please wait for them to be processed.')
        return redirect('adopter_apply_list')

    # Check if already applied for this pet
    if AdoptionApplication.objects.filter(adopter=adopter, pet=pet).exists():
        messages.error(request, f'You have already applied for {pet.name}.')
        return redirect('adopter_apply_list')

    if request.method == 'POST':
        # Check if user agreed to terms (waiver)
        agree_terms = request.POST.get('agree_terms')
        if not agree_terms:
            messages.error(request, 'You must agree to the adoption terms and conditions.')
            return render(request, 'adoptions/adopter_apply_form.html', {'pet': pet, 'adopter': adopter})

        notes = request.POST.get('notes', '')

        AdoptionApplication.objects.create(
            adopter=adopter,
            pet=pet,
            notes=notes,
            status='Pending'
        )

        messages.success(request, f'Your application for {pet.name} has been submitted!')
        return redirect('adopter_dashboard')

    return render(request, 'adoptions/adopter_apply_form.html', {'pet': pet, 'adopter': adopter})


def adopter_apply_list(request):
    """Page for adopters to see all available pets and apply"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    adopter = get_object_or_404(Adopter, adopter_id=request.session['adopter_id'])
    available_pets = Pet.objects.filter(status='Available')

    # Get pets the adopter has already applied for
    applied_pet_ids = AdoptionApplication.objects.filter(adopter=adopter).values_list('pet_id', flat=True)

    context = {
        'adopter': adopter,
        'available_pets': available_pets,
        'applied_pet_ids': applied_pet_ids,
    }
    return render(request, 'adoptions/adopter_apply_list.html', context)


# ==================== ADOPTER PROFILE MANAGEMENT ====================
def adopter_profile(request):
    """View adopter profile"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    try:
        adopter = Adopter.objects.get(adopter_id=request.session['adopter_id'])
    except Adopter.DoesNotExist:
        messages.error(request, 'Adopter not found.')
        return redirect('login')

    return render(request, 'adoptions/adopter_profile.html', {'adopter': adopter})


def adopter_profile_edit(request):
    """Edit adopter profile"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    try:
        adopter = Adopter.objects.get(adopter_id=request.session['adopter_id'])
    except Adopter.DoesNotExist:
        messages.error(request, 'Adopter not found.')
        return redirect('login')

    if request.method == 'POST':
        adopter.first_name = request.POST.get('first_name')
        adopter.last_name = request.POST.get('last_name')
        adopter.email = request.POST.get('email')
        adopter.phone = request.POST.get('phone')
        adopter.address = request.POST.get('address')
        adopter.occupation = request.POST.get('occupation')
        adopter.has_other_pets = request.POST.get('has_other_pets') == 'on'
        adopter.has_children = request.POST.get('has_children') == 'on'
        adopter.save()

        # Update session with new name
        request.session['adopter_name'] = f"{adopter.first_name} {adopter.last_name}"
        request.session['user_name'] = f"{adopter.first_name} {adopter.last_name}"
        request.session['user_email'] = adopter.email

        messages.success(request, 'Profile updated successfully!')
        return redirect('adopter_profile')

    return render(request, 'adoptions/adopter_profile_edit.html', {'adopter': adopter})


def adopter_change_password(request):
    """Change adopter password"""
    if 'adopter_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')

    try:
        adopter = Adopter.objects.get(adopter_id=request.session['adopter_id'])
    except Adopter.DoesNotExist:
        messages.error(request, 'Adopter not found.')
        return redirect('login')

    if request.method == 'POST':
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if not adopter.check_password(current):
            messages.error(request, 'Current password is incorrect.')
        elif new != confirm:
            messages.error(request, 'New passwords do not match.')
        elif len(new) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            adopter.set_password(new)
            adopter.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('login')

    return render(request, 'adoptions/adopter_change_password.html', {'adopter': adopter})


# ==================== TERMS AND WAIVER ====================
def terms_waiver(request):
    """Display the adoption waiver and terms of service"""
    return render(request, 'adoptions/terms_waiver.html')


# ==================== ADOPTION MANAGEMENT (STAFF ONLY) ====================
@login_required
def adoption_list(request):
    """List all adoptions - Staff only"""
    adoptions = Adoption.objects.all().order_by('-adoption_date')

    # Calculate total revenue from paid payments
    total_revenue = Payment.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0

    # Get pending applications count
    pending_applications = AdoptionApplication.objects.filter(status='Pending').count()

    context = {
        'adoptions': adoptions,
        'total_revenue': total_revenue,
        'pending_applications': pending_applications,
    }
    return render(request, 'adoptions/adoption_list.html', context)


@login_required
def adoption_add(request):
    """Add a new adoption record - Staff only"""
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        adopter_id = request.POST.get('adopter_id')
        adoption_date = request.POST.get('adoption_date')
        adoption_fee = request.POST.get('adoption_fee')

        pet = get_object_or_404(Pet, pet_id=pet_id)
        adopter = get_object_or_404(Adopter, adopter_id=adopter_id)

        # Create adoption record
        adoption = Adoption.objects.create(
            pet=pet,
            adopter=adopter,
            adoption_date=adoption_date,
            adoption_fee=adoption_fee,
            staff=request.user,
            status='Completed'
        )

        # Update pet status to adopted
        pet.status = 'Adopted'
        pet.save()

        messages.success(request, f'{pet.name} has been adopted by {adopter.first_name}!')
        return redirect('adoption_list')

    pets = Pet.objects.filter(status='Available')
    adopters = Adopter.objects.all()

    context = {
        'pets': pets,
        'adopters': adopters,
    }
    return render(request, 'adoptions/adoption_form.html', context)


@login_required
def adoption_edit(request, pk):
    """Edit an adoption record - Staff only"""
    adoption = get_object_or_404(Adoption, adoption_id=pk)

    if request.method == 'POST':
        adoption.adoption_fee = request.POST.get('adoption_fee')
        adoption.status = request.POST.get('status')
        adoption.save()
        messages.success(request, 'Adoption updated successfully!')
        return redirect('adoption_list')

    return render(request, 'adoptions/adoption_form.html', {'adoption': adoption})


@login_required
def adoption_delete(request, pk):
    """Delete an adoption record - Staff only"""
    adoption = get_object_or_404(Adoption, adoption_id=pk)

    if request.method == 'POST':
        pet_name = adoption.pet.name
        # Update pet status back to available
        adoption.pet.status = 'Available'
        adoption.pet.save()
        adoption.delete()
        messages.success(request, f'Adoption record for {pet_name} has been deleted.')
        return redirect('adoption_list')

    return render(request, 'adoptions/adoption_confirm_delete.html', {'adoption': adoption})


# ==================== APPLICATION MANAGEMENT (STAFF ONLY) ====================
@login_required
def application_list(request):
    """List all adoption applications - Staff only"""
    applications = AdoptionApplication.objects.all().order_by('-application_date')
    return render(request, 'adoptions/application_list.html', {'applications': applications})


@login_required
def application_add(request):
    """Add a new adoption application - Staff only"""
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        adopter_id = request.POST.get('adopter_id')
        notes = request.POST.get('notes', '')

        pet = get_object_or_404(Pet, pet_id=pet_id)
        adopter = get_object_or_404(Adopter, adopter_id=adopter_id)

        # Check if adopter has too many pending applications
        pending_count = AdoptionApplication.objects.filter(adopter=adopter, status='Pending').count()
        if pending_count >= 3:
            messages.error(request, 'This adopter already has 3 pending applications.')
            return redirect('application_list')

        # Check if pet is available
        if pet.status != 'Available':
            messages.error(request, f'{pet.name} is no longer available for adoption.')
            return redirect('application_list')

        application = AdoptionApplication.objects.create(
            pet=pet,
            adopter=adopter,
            staff=request.user,
            notes=notes,
            status='Pending'
        )

        messages.success(request, f'Application submitted for {pet.name}!')
        return redirect('application_list')

    pets = Pet.objects.filter(status='Available')
    adopters = Adopter.objects.all()

    context = {
        'pets': pets,
        'adopters': adopters,
    }
    return render(request, 'adoptions/application_form.html', context)


@login_required
def application_approve(request, pk):
    """Approve an adoption application - Staff only"""
    application = get_object_or_404(AdoptionApplication, application_id=pk)

    if request.method == 'POST':
        application.status = 'Approved'
        application.save()
        messages.success(request, f'Application for {application.pet.name} has been approved!')
        return redirect('application_list')

    return render(request, 'adoptions/application_approve.html', {'application': application})


@login_required
def application_reject(request, pk):
    """Reject an adoption application - Staff only"""
    application = get_object_or_404(AdoptionApplication, application_id=pk)

    if request.method == 'POST':
        application.status = 'Rejected'
        application.save()
        messages.warning(request, f'Application for {application.pet.name} has been rejected.')
        return redirect('application_list')

    return render(request, 'adoptions/application_reject.html', {'application': application})


# ==================== INTERVIEW MANAGEMENT (STAFF ONLY) ====================
@login_required
def interview_list(request):
    """List all interviews - Staff only"""
    interviews = Interview.objects.all().order_by('-interview_datetime')
    return render(request, 'adoptions/interview_list.html', {'interviews': interviews})


@login_required
def interview_add(request, application_id):
    """Schedule an interview for an application - Staff only"""
    application = get_object_or_404(AdoptionApplication, application_id=application_id)

    if request.method == 'POST':
        interview_datetime = request.POST.get('interview_datetime')
        remarks = request.POST.get('remarks', '')

        Interview.objects.create(
            application=application,
            staff=request.user,
            interview_datetime=interview_datetime,
            remarks=remarks
        )

        messages.success(request, f'Interview scheduled for {application.pet.name}!')
        return redirect('interview_list')

    return render(request, 'adoptions/interview_form.html', {'application': application})


@login_required
def interview_result(request, pk):
    """Update interview result - Staff only"""
    interview = get_object_or_404(Interview, interview_id=pk)

    if request.method == 'POST':
        result = request.POST.get('result')
        interview.result = result
        interview.save()
        messages.success(request, f'Interview result updated to {result}!')
        return redirect('interview_list')

    return render(request, 'adoptions/interview_result.html', {'interview': interview})


# ==================== HOME VISIT MANAGEMENT (STAFF ONLY) ====================
@login_required
def homevisit_list(request):
    """List all home visits - Staff only"""
    visits = HomeVisit.objects.all().order_by('-visit_date')
    return render(request, 'adoptions/homevisit_list.html', {'visits': visits})


@login_required
def homevisit_add(request, application_id):
    """Schedule a home visit for an application - Staff only"""
    application = get_object_or_404(AdoptionApplication, application_id=application_id)

    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')
        remarks = request.POST.get('remarks', '')

        HomeVisit.objects.create(
            application=application,
            staff=request.user,
            visit_date=visit_date,
            remarks=remarks
        )

        messages.success(request, f'Home visit scheduled for {application.pet.name}!')
        return redirect('homevisit_list')

    return render(request, 'adoptions/homevisit_form.html', {'application': application})


@login_required
def homevisit_result(request, pk):
    """Update home visit result - Staff only"""
    visit = get_object_or_404(HomeVisit, visit_id=pk)

    if request.method == 'POST':
        result = request.POST.get('result')
        visit.result = result
        visit.save()
        messages.success(request, f'Home visit result updated to {result}!')
        return redirect('homevisit_list')

    return render(request, 'adoptions/homevisit_result.html', {'visit': visit})


# ==================== PAYMENT MANAGEMENT (STAFF ONLY) ====================
@login_required
def payment_list(request):
    """List all payments - Staff only"""
    payments = Payment.objects.all().order_by('-payment_date')

    # Calculate total revenue
    total_revenue = Payment.objects.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'payments': payments,
        'total_revenue': total_revenue,
    }
    return render(request, 'adoptions/payment_list.html', context)


@login_required
def payment_add(request, adoption_id):
    """Record a payment for an adoption - Staff only"""
    adoption = get_object_or_404(Adoption, adoption_id=adoption_id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        reference_no = request.POST.get('reference_no', '')

        # Validate amount matches adoption fee
        if float(amount) != float(adoption.adoption_fee):
            messages.error(request, f'Payment amount must match the adoption fee (${adoption.adoption_fee}).')
            return redirect('payment_list')

        Payment.objects.create(
            adoption=adoption,
            amount=amount,
            method=method,
            reference_no=reference_no or f'PAY-{adoption.adoption_id}-{adoption.adopter.adopter_id}',
            status='Paid'
        )

        messages.success(request, f'Payment recorded for {adoption.pet.name}!')
        return redirect('payment_list')

    return render(request, 'adoptions/payment_form.html', {'adoption': adoption})