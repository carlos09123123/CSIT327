from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FosterAssignment
from apps.animals.models import Pet


# ==================== FOSTER ASSIGNMENT MANAGEMENT ====================
@login_required
def foster_list(request):
    """List all foster assignments"""
    active_fosters = FosterAssignment.objects.filter(status='Active').order_by('-start_date')
    completed_fosters = FosterAssignment.objects.filter(status='Completed').order_by('-end_date')
    cancelled_fosters = FosterAssignment.objects.filter(status='Cancelled').order_by('-start_date')

    context = {
        'active_fosters': active_fosters,
        'completed_fosters': completed_fosters,
        'cancelled_fosters': cancelled_fosters,
    }
    return render(request, 'fostering/foster_list.html', context)


@login_required
def foster_add(request):
    """Add a new foster assignment"""
    if request.method == 'POST':
        pet_id = request.POST.get('pet_id')
        foster_name = request.POST.get('foster_name')
        foster_phone = request.POST.get('foster_phone')
        foster_address = request.POST.get('foster_address')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        pet = get_object_or_404(Pet, pet_id=pet_id)

        # Business Rule: Check if pet already has an active foster assignment
        if FosterAssignment.objects.filter(pet=pet, status='Active').exists():
            messages.error(request,
                           f'{pet.name} already has an active foster assignment. A pet cannot have multiple active fosters simultaneously.')
            return redirect('foster_add')

        # Business Rule: End date must be after start date
        if end_date and end_date <= start_date:
            messages.error(request, 'End date must be after start date.')
            return redirect('foster_add')

        # Create foster assignment
        foster = FosterAssignment.objects.create(
            pet=pet,
            foster_name=foster_name,
            foster_phone=foster_phone,
            foster_address=foster_address,
            start_date=start_date,
            end_date=end_date if end_date else None,
            status='Active'
        )

        # Update pet status to Fostered
        pet.status = 'Fostered'
        pet.save()

        messages.success(request, f'{pet.name} has been assigned to foster family "{foster_name}"!')
        return redirect('foster_list')

    # Get available pets (not adopted and not already active fostered)
    available_pets = Pet.objects.filter(status__in=['Available', 'Fostered']).exclude(
        foster_assignments__status='Active'
    )

    context = {
        'pets': available_pets,
    }
    return render(request, 'fostering/foster_form.html', context)


@login_required
def foster_edit(request, pk):
    """Edit a foster assignment"""
    foster = get_object_or_404(FosterAssignment, foster_id=pk)

    if request.method == 'POST':
        foster_name = request.POST.get('foster_name')
        foster_phone = request.POST.get('foster_phone')
        foster_address = request.POST.get('foster_address')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')

        # Business Rule: End date must be after start date
        if end_date and end_date <= start_date:
            messages.error(request, 'End date must be after start date.')
            return redirect('foster_edit', pk=pk)

        # Update fields
        foster.foster_name = foster_name
        foster.foster_phone = foster_phone
        foster.foster_address = foster_address
        foster.start_date = start_date
        foster.end_date = end_date if end_date else None
        foster.status = status

        # Update pet status based on foster status
        if status == 'Active':
            foster.pet.status = 'Fostered'
        elif status in ['Completed', 'Cancelled']:
            foster.pet.status = 'Available'

        foster.pet.save()
        foster.save()

        messages.success(request, f'Foster assignment for {foster.pet.name} has been updated!')
        return redirect('foster_list')

    context = {
        'foster': foster,
        'pets': Pet.objects.all(),
    }
    return render(request, 'fostering/foster_form.html', context)


@login_required
def foster_delete(request, pk):
    """Delete/cancel a foster assignment"""
    foster = get_object_or_404(FosterAssignment, foster_id=pk)

    if request.method == 'POST':
        pet_name = foster.pet.name

        # Update pet status back to available
        foster.pet.status = 'Available'
        foster.pet.save()

        foster.delete()
        messages.success(request, f'Foster assignment for {pet_name} has been cancelled.')
        return redirect('foster_list')

    return render(request, 'fostering/foster_confirm_delete.html', {'foster': foster})


@login_required
def foster_end(request, pk):
    """End an active foster assignment (mark as completed)"""
    foster = get_object_or_404(FosterAssignment, foster_id=pk)

    if request.method == 'POST':
        foster.status = 'Completed'
        foster.end_date = timezone.now().date()
        foster.pet.status = 'Available'
        foster.pet.save()
        foster.save()

        messages.success(request,
                         f'Foster assignment for {foster.pet.name} has been completed. The pet is now available for adoption.')
        return redirect('foster_list')

    return render(request, 'fostering/foster_end.html', {'foster': foster})