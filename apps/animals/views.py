from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from datetime import date, timedelta
from .models import Pet, MedicalRecord, Vaccination, Veterinary


# ==================== HELPER FUNCTIONS ====================
def get_user_permission(request):
    """Determine what permissions the user has"""
    if not request.user.is_authenticated:
        return None

    role = request.user.role
    if role == 'Admin':
        return 'full_access'
    elif role in ['Manager', 'Staff']:
        return 'staff_access'
    elif role == 'Vet':
        return 'vet_access'
    return None


def check_vet_medical_permission(request):
    """Check if user can access medical records"""
    permission = get_user_permission(request)
    if permission in ['full_access', 'staff_access', 'vet_access']:
        return True
    raise PermissionDenied("You don't have permission to access medical records.")


def check_pet_management_permission(request):
    """Check if user can manage pets (add/edit/delete)"""
    permission = get_user_permission(request)
    if permission in ['full_access', 'staff_access']:
        return True
    raise PermissionDenied("Only staff can manage pets.")


# ==================== PET VIEWS ====================
@login_required
def pet_list(request):
    """List all pets - All staff types can view"""
    permission = get_user_permission(request)
    if not permission:
        raise PermissionDenied("You don't have permission to view pets.")

    pets = Pet.objects.all().order_by('-intake_date')
    is_vet = (permission == 'vet_access')

    return render(request, 'animals/pet_list.html', {
        'pets': pets,
        'is_vet': is_vet,
        'user_role': request.user.role
    })


@login_required
def pet_detail(request, pk):
    """View pet details - All staff types can view"""
    permission = get_user_permission(request)
    if not permission:
        raise PermissionDenied("You don't have permission to view pet details.")

    pet = get_object_or_404(Pet, pet_id=pk)
    medical_records = pet.medical_records.all().order_by('-visit_date')
    vaccinations = pet.vaccinations.all().order_by('-vaccination_date')
    is_vet = (permission == 'vet_access')

    return render(request, 'animals/pet_detail.html', {
        'pet': pet,
        'medical_records': medical_records,
        'vaccinations': vaccinations,
        'is_vet': is_vet,
        'user_role': request.user.role
    })


@login_required
def pet_add(request):
    """Add a new pet - Only Admin/Manager/Staff (NOT Veterinarian)"""
    check_pet_management_permission(request)

    if request.method == 'POST':
        pet = Pet.objects.create(
            name=request.POST.get('name'),
            species=request.POST.get('species'),
            breed=request.POST.get('breed', ''),
            age=request.POST.get('age'),
            sex=request.POST.get('sex'),
            size=request.POST.get('size'),
            color=request.POST.get('color'),
            vaccination_status=request.POST.get('vaccination_status') == 'on',
            spay_neuter_status=request.POST.get('spay_neuter_status') == 'on',
            medical_notes=request.POST.get('medical_notes', ''),
            status=request.POST.get('status'),
        )
        messages.success(request, f'Pet "{pet.name}" added successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    context = {
        'species_choices': Pet.SPECIES_CHOICES,
        'sex_choices': Pet.SEX_CHOICES,
        'size_choices': Pet.SIZE_CHOICES,
        'status_choices': Pet.STATUS_CHOICES,
    }
    return render(request, 'animals/pet_form.html', context)


@login_required
def pet_edit(request, pk):
    """Edit a pet - Only Admin/Manager/Staff (NOT Veterinarian)"""
    check_pet_management_permission(request)

    pet = get_object_or_404(Pet, pet_id=pk)

    if request.method == 'POST':
        pet.name = request.POST.get('name')
        pet.species = request.POST.get('species')
        pet.breed = request.POST.get('breed', '')
        pet.age = request.POST.get('age')
        pet.sex = request.POST.get('sex')
        pet.size = request.POST.get('size')
        pet.color = request.POST.get('color')
        pet.vaccination_status = request.POST.get('vaccination_status') == 'on'
        pet.spay_neuter_status = request.POST.get('spay_neuter_status') == 'on'
        pet.medical_notes = request.POST.get('medical_notes', '')
        pet.status = request.POST.get('status')
        pet.save()
        messages.success(request, f'Pet "{pet.name}" updated successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    context = {
        'pet': pet,
        'species_choices': Pet.SPECIES_CHOICES,
        'sex_choices': Pet.SEX_CHOICES,
        'size_choices': Pet.SIZE_CHOICES,
        'status_choices': Pet.STATUS_CHOICES,
    }
    return render(request, 'animals/pet_form.html', context)


@login_required
def pet_delete(request, pk):
    """Delete a pet - Only Admin/Manager/Staff (NOT Veterinarian)"""
    check_pet_management_permission(request)

    pet = get_object_or_404(Pet, pet_id=pk)

    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'Pet "{pet_name}" deleted successfully!')
        return redirect('pet_list')

    return render(request, 'animals/pet_confirm_delete.html', {'pet': pet})


# ==================== MEDICAL RECORD VIEWS ====================
@login_required
def medical_add(request, pet_id):
    """Add medical record - Vets, Staff, Admin can add"""
    check_vet_medical_permission(request)

    pet = get_object_or_404(Pet, pet_id=pet_id)

    if request.method == 'POST':
        MedicalRecord.objects.create(
            pet=pet,
            vet_id=request.POST.get('vet_id') or None,
            visit_date=request.POST.get('visit_date'),
            diagnosis=request.POST.get('diagnosis'),
            treatment=request.POST.get('treatment'),
            weight=request.POST.get('weight') or None,
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Medical record added successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    vets = Veterinary.objects.all()
    return render(request, 'animals/medical_form.html', {'pet': pet, 'vets': vets})


@login_required
def medical_delete(request, pk):
    """Delete medical record - Staff/Admin only (Vets cannot delete)"""
    permission = get_user_permission(request)
    if permission not in ['full_access', 'staff_access']:
        raise PermissionDenied("Only staff can delete medical records.")

    record = get_object_or_404(MedicalRecord, medical_id=pk)
    pet_id = record.pet.pet_id
    record.delete()
    messages.success(request, 'Medical record deleted!')
    return redirect('pet_detail', pk=pet_id)


@login_required
def medical_record_list(request):
    """List all medical records - Veterinarians can view"""
    permission = get_user_permission(request)
    if not permission:
        raise PermissionDenied("You don't have permission to view medical records.")

    records = MedicalRecord.objects.all().order_by('-visit_date')

    search_query = request.GET.get('search', '')
    if search_query:
        records = records.filter(pet__name__icontains=search_query)

    diagnosis_filter = request.GET.get('diagnosis', '')
    if diagnosis_filter:
        records = records.filter(diagnosis__icontains=diagnosis_filter)

    date_range = request.GET.get('date_range', '')
    today = date.today()
    if date_range == 'week':
        week_ago = today - timedelta(days=7)
        records = records.filter(visit_date__gte=week_ago)
    elif date_range == 'month':
        month_ago = today - timedelta(days=30)
        records = records.filter(visit_date__gte=month_ago)
    elif date_range == 'year':
        year_ago = today - timedelta(days=365)
        records = records.filter(visit_date__gte=year_ago)

    common_diagnoses = MedicalRecord.objects.values('diagnosis').annotate(
        count=Count('diagnosis')
    ).order_by('-count')[:10]

    total_records = MedicalRecord.objects.count()
    records_this_month = MedicalRecord.objects.filter(
        visit_date__gte=today.replace(day=1)
    ).count()
    records_this_week = MedicalRecord.objects.filter(
        visit_date__gte=today - timedelta(days=7)
    ).count()
    pets_with_records = Pet.objects.filter(medical_records__isnull=False).distinct().count()

    context = {
        'records': records,
        'search_query': search_query,
        'diagnosis_filter': diagnosis_filter,
        'date_range': date_range,
        'common_diagnoses': common_diagnoses,
        'total_records': total_records,
        'records_this_month': records_this_month,
        'records_this_week': records_this_week,
        'pets_with_records': pets_with_records,
        'is_vet': get_user_permission(request) == 'vet_access',
        'user_role': request.user.role,
    }

    return render(request, 'animals/medical_record_list.html', context)


# ==================== VACCINATION VIEWS ====================
@login_required
def vaccination_add(request, pet_id):
    """Add vaccination - Vets, Staff, Admin can add"""
    check_vet_medical_permission(request)

    pet = get_object_or_404(Pet, pet_id=pet_id)

    if request.method == 'POST':
        Vaccination.objects.create(
            pet=pet,
            vet_id=request.POST.get('vet_id') or None,
            vaccine_name=request.POST.get('vaccine_name'),
            dose_no=request.POST.get('dose_no'),
            vaccination_date=request.POST.get('vaccination_date'),
            next_due_date=request.POST.get('next_due_date'),
        )
        pet.vaccination_status = True
        pet.save()
        messages.success(request, 'Vaccination record added successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    vets = Veterinary.objects.all()
    return render(request, 'animals/vaccination_form.html', {'pet': pet, 'vets': vets})


@login_required
def vaccination_delete(request, pk):
    """Delete vaccination - Staff/Admin only (Vets cannot delete)"""
    permission = get_user_permission(request)
    if permission not in ['full_access', 'staff_access']:
        raise PermissionDenied("Only staff can delete vaccination records.")

    vacc = get_object_or_404(Vaccination, vaccination_id=pk)
    pet_id = vacc.pet.pet_id
    vacc.delete()
    messages.success(request, 'Vaccination record deleted!')
    return redirect('pet_detail', pk=pet_id)


# ==================== VETERINARY MANAGEMENT ====================
@login_required
def vet_list(request):
    """List veterinarians - Show staff members with role 'Vet' from accounts"""
    permission = get_user_permission(request)
    if not permission:
        raise PermissionDenied("You don't have permission to view veterinarians.")

    # Get staff members who have role = 'Vet' from accounts app
    from apps.accounts.models import Staff
    vets = Staff.objects.filter(role='Vet', status=True)

    return render(request, 'animals/vet_list.html', {'vets': vets})


@login_required
def vet_add(request):
    """Add veterinarian - Only Admin/Manager/Staff"""
    permission = get_user_permission(request)
    if permission not in ['full_access', 'staff_access']:
        raise PermissionDenied("Only staff can add veterinarians.")

    if request.method == 'POST':
        Veterinary.objects.create(
            full_name=request.POST.get('full_name'),
            clinic_name=request.POST.get('clinic_name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            license_no=request.POST.get('license_no'),
        )
        messages.success(request, 'Veterinarian added successfully!')
        return redirect('vet_list')
    return render(request, 'animals/vet_form.html')


@login_required
def vet_delete(request, pk):
    """Delete veterinarian - Only Admin/Manager/Staff"""
    permission = get_user_permission(request)
    if permission not in ['full_access', 'staff_access']:
        raise PermissionDenied("Only staff can delete veterinarians.")

    vet = get_object_or_404(Veterinary, vet_id=pk)
    vet.delete()
    messages.success(request, 'Veterinarian deleted!')
    return redirect('vet_list')


# ==================== MEDICAL STATISTICS ====================
@login_required
def medical_statistics(request):
    """Medical statistics dashboard for veterinarians"""
    if request.user.role not in ['Admin', 'Manager', 'Staff', 'Vet']:
        raise PermissionDenied("You don't have permission to view medical statistics.")

    today = date.today()
    next_30_days = today + timedelta(days=30)
    last_30_days = today - timedelta(days=30)

    total_pets = Pet.objects.count()
    pets_with_medical = Pet.objects.filter(medical_notes__isnull=False).exclude(medical_notes='').count()
    under_medical_care = Pet.objects.filter(status='Medical').count()
    unvaccinated_pets = Pet.objects.filter(vaccination_status=False).count()

    upcoming_vaccinations = Vaccination.objects.filter(
        next_due_date__gte=today,
        next_due_date__lte=next_30_days
    )
    upcoming_count = upcoming_vaccinations.count()
    overdue_vaccinations = Vaccination.objects.filter(next_due_date__lt=today)
    overdue_count = overdue_vaccinations.count()
    completed_vaccinations = Vaccination.objects.filter(vaccination_date__lte=today).count()

    recent_medical = MedicalRecord.objects.filter(visit_date__gte=last_30_days).order_by('-visit_date')[:10]
    recent_count = MedicalRecord.objects.filter(visit_date__gte=last_30_days).count()
    total_medical_records = MedicalRecord.objects.count()

    common_diagnoses = MedicalRecord.objects.values('diagnosis').annotate(
        count=Count('diagnosis')
    ).order_by('-count')[:5]

    pets_by_status = {
        'Available': Pet.objects.filter(status='Available').count(),
        'Adopted': Pet.objects.filter(status='Adopted').count(),
        'Medical': Pet.objects.filter(status='Medical').count(),
        'Quarantine': Pet.objects.filter(status='Quarantine').count(),
    }

    pets_by_species = {
        'Dog': Pet.objects.filter(species='Dog').count(),
        'Cat': Pet.objects.filter(species='Cat').count(),
        'Other': Pet.objects.filter(species__in=['Bird', 'Rabbit', 'Other']).count(),
    }

    upcoming_vaccinations_list = []
    for vacc in upcoming_vaccinations[:10]:
        upcoming_vaccinations_list.append({
            'pet_name': vacc.pet.name,
            'vaccine_name': vacc.vaccine_name,
            'due_date': vacc.next_due_date,
            'days_left': (vacc.next_due_date - today).days,
        })

    overdue_vaccinations_list = []
    for vacc in overdue_vaccinations[:10]:
        overdue_vaccinations_list.append({
            'pet_name': vacc.pet.name,
            'vaccine_name': vacc.vaccine_name,
            'due_date': vacc.next_due_date,
            'days_overdue': (today - vacc.next_due_date).days,
        })

    recent_medical_list = []
    for record in recent_medical:
        recent_medical_list.append({
            'pet_name': record.pet.name,
            'visit_date': record.visit_date,
            'diagnosis': record.diagnosis[:50],
            'treatment': record.treatment[:50],
            'vet_name': record.vet.full_name if record.vet else 'Unknown',
        })

    common_diagnoses_list = []
    for diag in common_diagnoses:
        common_diagnoses_list.append({
            'name': diag['diagnosis'][:40],
            'count': diag['count'],
        })

    context = {
        'user': request.user,
        'is_vet': request.user.role == 'Vet',
        'total_pets': total_pets,
        'pets_with_medical': pets_with_medical,
        'under_medical_care': under_medical_care,
        'unvaccinated_pets': unvaccinated_pets,
        'upcoming_count': upcoming_count,
        'overdue_count': overdue_count,
        'completed_vaccinations': completed_vaccinations,
        'recent_count': recent_count,
        'total_medical_records': total_medical_records,
        'upcoming_vaccinations': upcoming_vaccinations_list,
        'overdue_vaccinations': overdue_vaccinations_list,
        'recent_medical_records': recent_medical_list,
        'common_diagnoses': common_diagnoses_list,
        'pets_by_status': pets_by_status,
        'pets_by_species': pets_by_species,
    }

    return render(request, 'animals/medical_statistics.html', context)