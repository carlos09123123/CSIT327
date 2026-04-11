from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet


# ==================== PET VIEWS ====================
@login_required
def pet_list(request):
    pets = Pet.objects.all().order_by('-intake_date')
    return render(request, 'animals/pet_list.html', {'pets': pets})


@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pet_id=pk)
    return render(request, 'animals/pet_detail.html', {'pet': pet})


@login_required
def pet_add(request):
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
    pet = get_object_or_404(Pet, pet_id=pk)

    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'Pet "{pet_name}" deleted successfully!')
        return redirect('pet_list')

    return render(request, 'animals/pet_confirm_delete.html', {'pet': pet})