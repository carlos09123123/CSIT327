from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Foster, FosterApplication, FosterAssignment, FosterCheckIn
from .forms import FosterForm, FosterApplicationForm, FosterAssignmentForm, FosterCheckInForm
from apps.animals.models import Pet

@login_required
def index(request):
    """Dashboard for fostering management"""
    active_assignments = FosterAssignment.objects.filter(status='Active').select_related('pet', 'foster')
    pending_applications = FosterApplication.objects.filter(status='Pending')
    recent_checkins = FosterCheckIn.objects.select_related('assignment__pet', 'assignment__foster').order_by('-checkin_date')[:5]

    context = {
        'active_assignments': active_assignments,
        'pending_applications': pending_applications,
        'recent_checkins': recent_checkins,
    }
    return render(request, 'fostering/index.html', context)

# Foster Views
@login_required
def foster_list(request):
    fosters = Foster.objects.all().order_by('last_name', 'first_name')
    return render(request, 'fostering/foster_list.html', {'fosters': fosters})

@login_required
def foster_add(request):
    if request.method == 'POST':
        form = FosterForm(request.POST)
        if form.is_valid():
            foster = form.save()
            messages.success(request, f'Foster "{foster.first_name} {foster.last_name}" added successfully!')
            return redirect('foster_detail', pk=foster.foster_id)
    else:
        form = FosterForm()
    return render(request, 'fostering/addNewFoster.html', {'form': form, 'title': 'Add Foster'})

@login_required
def foster_detail(request, pk):
    foster = get_object_or_404(Foster, foster_id=pk)
    applications = foster.applications.all().order_by('-application_date')
    assignments = foster.assignments.all().order_by('-start_date')
    return render(request, 'fostering/foster_detail.html', {
        'foster': foster,
        'applications': applications,
        'assignments': assignments,
    })

@login_required
def foster_edit(request, pk):
    foster = get_object_or_404(Foster, foster_id=pk)
    if request.method == 'POST':
        form = FosterForm(request.POST, instance=foster)
        if form.is_valid():
            foster = form.save()
            messages.success(request, f'Foster "{foster.first_name} {foster.last_name}" updated successfully!')
            return redirect('foster_detail', pk=foster.foster_id)
    else:
        form = FosterForm(instance=foster)
    return render(request, 'fostering/foster_form.html', {'form': form, 'foster': foster, 'title': 'Edit Foster'})

@login_required
def foster_delete(request, pk):
    foster = get_object_or_404(Foster, foster_id=pk)
    if request.method == 'POST':
        foster_name = f"{foster.first_name} {foster.last_name}"
        foster.delete()
        messages.success(request, f'Foster "{foster_name}" deleted successfully!')
        return redirect('foster_list')
    return render(request, 'fostering/foster_confirm_delete.html', {'foster': foster})

# Foster Application Views
@login_required
def application_list(request):
    applications = FosterApplication.objects.select_related('foster', 'staff').order_by('-application_date')
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    return render(request, 'fostering/application_list.html', {
        'applications': applications,
        'status_choices': FosterApplication.STATUS_CHOICES,
        'current_status': status_filter,
    })

@login_required
def application_add(request):
    if request.method == 'POST':
        form = FosterApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.staff = request.user
            application.save()
            messages.success(request, f'Application for {application.foster.first_name} {application.foster.last_name} added successfully!')
            return redirect('application_detail', pk=application.application_id)
    else:
        form = FosterApplicationForm()
    return render(request, 'fostering/application_form.html', {'form': form, 'title': 'Add Foster Application'})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(FosterApplication, application_id=pk)
    return render(request, 'fostering/application_detail.html', {'application': application})

@login_required
def application_edit(request, pk):
    application = get_object_or_404(FosterApplication, application_id=pk)
    if request.method == 'POST':
        form = FosterApplicationForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save()
            messages.success(request, f'Application for {application.foster.first_name} {application.foster.last_name} updated successfully!')
            return redirect('application_detail', pk=application.application_id)
    else:
        form = FosterApplicationForm(instance=application)
    return render(request, 'fostering/application_form.html', {'form': form, 'application': application, 'title': 'Edit Foster Application'})

@login_required
def application_delete(request, pk):
    application = get_object_or_404(FosterApplication, application_id=pk)
    if request.method == 'POST':
        foster_name = f"{application.foster.first_name} {application.foster.last_name}"
        application.delete()
        messages.success(request, f'Application for {foster_name} deleted successfully!')
        return redirect('application_list')
    return render(request, 'fostering/application_confirm_delete.html', {'application': application})

# Foster Assignment Views
@login_required
def assignment_list(request):
    assignments = FosterAssignment.objects.select_related('pet', 'foster', 'staff').order_by('-start_date')
    status_filter = request.GET.get('status')
    if status_filter:
        assignments = assignments.filter(status=status_filter)
    return render(request, 'fostering/assignment_list.html', {
        'assignments': assignments,
        'status_choices': FosterAssignment.STATUS_CHOICES,
        'current_status': status_filter,
    })

@login_required
def assignment_add(request):
    if request.method == 'POST':
        form = FosterAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.staff = request.user
            assignment.save()
            # Update pet status to 'Fostered'
            assignment.pet.status = 'Fostered'
            assignment.pet.save()
            messages.success(request, f'Assignment for {assignment.pet.name} created successfully!')
            return redirect('assignment_detail', pk=assignment.assignment_id)
    else:
        form = FosterAssignmentForm()
    return render(request, 'fostering/assignment_form.html', {'form': form, 'title': 'Add Foster Assignment'})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(FosterAssignment, assignment_id=pk)
    checkins = assignment.checkins.all().order_by('-checkin_date')
    return render(request, 'fostering/assignment_detail.html', {
        'assignment': assignment,
        'checkins': checkins,
    })

@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(FosterAssignment, assignment_id=pk)
    if request.method == 'POST':
        form = FosterAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            old_status = assignment.status
            assignment = form.save()
            # Update pet status based on assignment status
            if assignment.status == 'Completed' and old_status == 'Active':
                assignment.pet.status = 'Available'
                assignment.pet.save()
            elif assignment.status == 'Active' and old_status != 'Active':
                assignment.pet.status = 'Fostered'
                assignment.pet.save()
            messages.success(request, f'Assignment for {assignment.pet.name} updated successfully!')
            return redirect('assignment_detail', pk=assignment.assignment_id)
    else:
        form = FosterAssignmentForm(instance=assignment)
    return render(request, 'fostering/assignment_form.html', {'form': form, 'assignment': assignment, 'title': 'Edit Foster Assignment'})

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(FosterAssignment, assignment_id=pk)
    if request.method == 'POST':
        pet_name = assignment.pet.name
        # Update pet status back to Available if assignment was active
        if assignment.status == 'Active':
            assignment.pet.status = 'Available'
            assignment.pet.save()
        assignment.delete()
        messages.success(request, f'Assignment for "{pet_name}" deleted successfully!')
        return redirect('assignment_list')
    return render(request, 'fostering/assignment_confirm_delete.html', {'assignment': assignment})

# Foster Check-in Views
@login_required
def checkin_add(request, assignment_id):
    assignment = get_object_or_404(FosterAssignment, assignment_id=assignment_id)
    if request.method == 'POST':
        form = FosterCheckInForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.assignment = assignment
            checkin.staff = request.user
            checkin.save()
            messages.success(request, f'Check-in for {assignment.pet.name} added successfully!')
            return redirect('assignment_detail', pk=assignment.assignment_id)
    else:
        form = FosterCheckInForm()
    return render(request, 'fostering/checkin_form.html', {'form': form, 'assignment': assignment, 'title': 'Add Check-in'})

@login_required
def checkin_edit(request, pk):
    checkin = get_object_or_404(FosterCheckIn, checkin_id=pk)
    if request.method == 'POST':
        form = FosterCheckInForm(request.POST, instance=checkin)
        if form.is_valid():
            checkin = form.save()
            messages.success(request, f'Check-in updated successfully!')
            return redirect('assignment_detail', pk=checkin.assignment.assignment_id)
    else:
        form = FosterCheckInForm(instance=checkin)
    return render(request, 'fostering/checkin_form.html', {'form': form, 'checkin': checkin, 'assignment': checkin.assignment, 'title': 'Edit Check-in'})

@login_required
def checkin_delete(request, pk):
    checkin = get_object_or_404(FosterCheckIn, checkin_id=pk)
    assignment_id = checkin.assignment.assignment_id
    checkin.delete()
    messages.success(request, 'Check-in deleted successfully!')
    return redirect('assignment_detail', pk=assignment_id)
