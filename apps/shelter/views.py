from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShelterBranch, KennelCage, IntakeRecord
from apps.animals.models import Pet
from apps.accounts.models import Staff


# ==================== SHELTER BRANCH MANAGEMENT ====================
@login_required
def shelter_list(request):
    """List all shelter branches"""
    shelters = ShelterBranch.objects.all().order_by('name')
    return render(request, 'shelter/shelter_list.html', {'shelters': shelters})


@login_required
def shelter_add(request):
    """Add a new shelter branch"""
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Validate unique name
        if ShelterBranch.objects.filter(name=name).exists():
            messages.error(request, 'A branch with this name already exists.')
            return render(request, 'shelter/shelter_form.html')

        # Validate unique email
        if ShelterBranch.objects.filter(email=email).exists():
            messages.error(request, 'A branch with this email already exists.')
            return render(request, 'shelter/shelter_form.html')

        shelter = ShelterBranch.objects.create(
            name=name,
            address=address,
            city=city,
            contact_number=contact_number,
            email=email
        )
        messages.success(request, f'Branch "{shelter.name}" has been added successfully!')
        return redirect('shelter_list')

    return render(request, 'shelter/shelter_form.html')


@login_required
def shelter_edit(request, pk):
    """Edit a shelter branch"""
    shelter = get_object_or_404(ShelterBranch, shelter_id=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Check unique name (excluding current)
        if ShelterBranch.objects.filter(name=name).exclude(shelter_id=pk).exists():
            messages.error(request, 'A branch with this name already exists.')
            return render(request, 'shelter/shelter_form.html', {'shelter': shelter})

        # Check unique email (excluding current)
        if ShelterBranch.objects.filter(email=email).exclude(shelter_id=pk).exists():
            messages.error(request, 'A branch with this email already exists.')
            return render(request, 'shelter/shelter_form.html', {'shelter': shelter})

        shelter.name = name
        shelter.address = address
        shelter.city = city
        shelter.contact_number = contact_number
        shelter.email = email
        shelter.save()

        messages.success(request, f'Branch "{shelter.name}" has been updated successfully!')
        return redirect('shelter_list')

    return render(request, 'shelter/shelter_form.html', {'shelter': shelter})


@login_required
def shelter_delete(request, pk):
    """Delete a shelter branch"""
    shelter = get_object_or_404(ShelterBranch, shelter_id=pk)

    if request.method == 'POST':
        shelter_name = shelter.name
        shelter.delete()
        messages.success(request, f'Branch "{shelter_name}" has been deleted successfully!')
        return redirect('shelter_list')

    return render(request, 'shelter/shelter_confirm_delete.html', {'shelter': shelter})


# ==================== KENNEL/CAGE MANAGEMENT ====================
@login_required
def kennel_list(request, shelter_id=None):
    """List all kennels, optionally filtered by shelter"""
    if shelter_id:
        shelter = get_object_or_404(ShelterBranch, shelter_id=shelter_id)
        kennels = KennelCage.objects.filter(shelter=shelter).order_by('kennel_code')
    else:
        kennels = KennelCage.objects.all().order_by('shelter__name', 'kennel_code')
        shelter = None

    shelters = ShelterBranch.objects.all()
    return render(request, 'shelter/kennel_list.html', {
        'kennels': kennels,
        'shelters': shelters,
        'selected_shelter': shelter
    })


@login_required
def kennel_add(request):
    """Add a new kennel/cage"""
    if request.method == 'POST':
        shelter_id = request.POST.get('shelter_id')
        kennel_code = request.POST.get('kennel_code')
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        status = request.POST.get('status')

        shelter = get_object_or_404(ShelterBranch, shelter_id=shelter_id)

        # Check unique kennel_code within shelter
        if KennelCage.objects.filter(shelter=shelter, kennel_code=kennel_code).exists():
            messages.error(request, f'Kennel code "{kennel_code}" already exists in this shelter.')
            return redirect('kennel_list')

        kennel = KennelCage.objects.create(
            shelter=shelter,
            kennel_code=kennel_code,
            type=type,
            capacity=capacity,
            current_occupancy=0,
            status=status
        )
        messages.success(request, f'Kennel "{kennel.kennel_code}" has been added successfully!')
        return redirect('kennel_list')

    shelters = ShelterBranch.objects.all()
    return render(request, 'shelter/kennel_form.html', {'shelters': shelters})


@login_required
def kennel_edit(request, pk):
    """Edit a kennel/cage"""
    kennel = get_object_or_404(KennelCage, kennel_id=pk)

    if request.method == 'POST':
        kennel_code = request.POST.get('kennel_code')
        type = request.POST.get('type')
        capacity = request.POST.get('capacity')
        current_occupancy = request.POST.get('current_occupancy')
        status = request.POST.get('status')

        # Check unique kennel_code within shelter (excluding current)
        if KennelCage.objects.filter(shelter=kennel.shelter, kennel_code=kennel_code).exclude(kennel_id=pk).exists():
            messages.error(request, f'Kennel code "{kennel_code}" already exists in this shelter.')
            return render(request, 'shelter/kennel_form.html',
                          {'kennel': kennel, 'shelters': ShelterBranch.objects.all()})

        # Validate occupancy doesn't exceed capacity
        if int(current_occupancy) > int(capacity):
            messages.error(request, 'Current occupancy cannot exceed capacity.')
            return render(request, 'shelter/kennel_form.html',
                          {'kennel': kennel, 'shelters': ShelterBranch.objects.all()})

        # Validate no animals in maintenance kennel
        if status == 'Maintenance' and int(current_occupancy) > 0:
            messages.error(request, 'Cannot have animals in a maintenance kennel.')
            return render(request, 'shelter/kennel_form.html',
                          {'kennel': kennel, 'shelters': ShelterBranch.objects.all()})

        kennel.kennel_code = kennel_code
        kennel.type = type
        kennel.capacity = capacity
        kennel.current_occupancy = current_occupancy
        kennel.status = status
        kennel.save()

        messages.success(request, f'Kennel "{kennel.kennel_code}" has been updated successfully!')
        return redirect('kennel_list')

    shelters = ShelterBranch.objects.all()
    return render(request, 'shelter/kennel_form.html', {'kennel': kennel, 'shelters': shelters})


@login_required
def kennel_delete(request, pk):
    """Delete a kennel/cage"""
    kennel = get_object_or_404(KennelCage, kennel_id=pk)

    if request.method == 'POST':
        kennel_code = kennel.kennel_code
        kennel.delete()
        messages.success(request, f'Kennel "{kennel_code}" has been deleted successfully!')
        return redirect('kennel_list')

    return render(request, 'shelter/kennel_confirm_delete.html', {'kennel': kennel})


# ==================== INTAKE RECORD MANAGEMENT ====================
@login_required
def intake_list(request):
    """List all intake records"""
    intakes = IntakeRecord.objects.all().order_by('-intake_date')
    return render(request, 'shelter/intake_list.html', {'intakes': intakes})


@login_required
def intake_add(request):
    """Add a new intake record"""
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        shelter_id = request.POST.get('shelter_id')
        staff_id = request.POST.get('staff_id')
        intake_type = request.POST.get('intake_type')
        condition_notes = request.POST.get('condition_notes', '')
        notes = request.POST.get('notes', '')

        pet = get_object_or_404(Pet, pet_id=pet_id)
        shelter = get_object_or_404(ShelterBranch, shelter_id=shelter_id)
        staff = get_object_or_404(Staff, staff_id=staff_id) if staff_id else None

        # Check if pet already has an intake record
        if IntakeRecord.objects.filter(pet=pet).exists():
            messages.error(request, f'{pet.name} already has an intake record.')
            return redirect('intake_list')

        intake = IntakeRecord.objects.create(
            pet=pet,
            shelter=shelter,
            staff=staff,
            intake_type=intake_type,
            condition_notes=condition_notes,
            notes=notes
        )

        # Update pet status to Available
        pet.status = 'Available'
        pet.save()

        messages.success(request, f'Intake record for {pet.name} has been created!')
        return redirect('intake_list')

    pets = Pet.objects.filter(status__in=['Available', 'Medical'])
    shelters = ShelterBranch.objects.all()
    staff_members = Staff.objects.filter(status=True)

    return render(request, 'shelter/intake_form.html', {
        'pets': pets,
        'shelters': shelters,
        'staff_members': staff_members
    })


@login_required
def intake_edit(request, pk):
    """Edit an intake record"""
    intake = get_object_or_404(IntakeRecord, intake_id=pk)

    if request.method == 'POST':
        intake.intake_type = request.POST.get('intake_type')
        intake.condition_notes = request.POST.get('condition_notes', '')
        intake.notes = request.POST.get('notes', '')
        intake.save()

        messages.success(request, f'Intake record for {intake.pet.name} has been updated!')
        return redirect('intake_list')

    return render(request, 'shelter/intake_form.html', {'intake': intake})


@login_required
def intake_delete(request, pk):
    """Delete an intake record"""
    intake = get_object_or_404(IntakeRecord, intake_id=pk)

    if request.method == 'POST':
        pet_name = intake.pet.name
        intake.delete()
        messages.success(request, f'Intake record for {pet_name} has been deleted!')
        return redirect('intake_list')

    return render(request, 'shelter/intake_confirm_delete.html', {'intake': intake})