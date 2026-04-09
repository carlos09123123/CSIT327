from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet, MedicalRecord, Vaccination, Veterinary


# Pet Views
@login_required
def pet_list(request):
    pets = Pet.objects.all().order_by('-intake_date')
    status_filter = request.GET.get('status')
    species_filter = request.GET.get('species')

    if status_filter:
        pets = pets.filter(status=status_filter)
    if species_filter:
        pets = pets.filter(species=species_filter)

    context = {
        'pets': pets,
        'status_choices': Pet.STATUS_CHOICES,
        'species_choices': Pet.SPECIES_CHOICES,
        'current_status': status_filter,
        'current_species': species_filter,
    }
    return render(request, 'animals/pet_list.html', context)


@login_required
def pet_add(request):
    if request.method == 'POST':
        pet = Pet.objects.create(
            name=request.POST['name'],
            species=request.POST['species'],
            breed=request.POST.get('breed', ''),
            age=request.POST['age'],
            sex=request.POST['sex'],
            size=request.POST['size'],
            color=request.POST['color'],
            vaccination_status=request.POST.get('vaccination_status') == 'on',
            spay_neuter_status=request.POST.get('spay_neuter_status') == 'on',
            medical_notes=request.POST.get('medical_notes', ''),
            status=request.POST['status'],
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
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pet_id=pk)
    medical_records = pet.medical_records.all().order_by('-visit_date')
    vaccinations = pet.vaccinations.all().order_by('-vaccination_date')
    return render(request, 'animals/pet_detail.html', {
        'pet': pet,
        'medical_records': medical_records,
        'vaccinations': vaccinations,
    })


@login_required
def pet_edit(request, pk):
    pet = get_object_or_404(Pet, pet_id=pk)
    if request.method == 'POST':
        pet.name = request.POST['name']
        pet.species = request.POST['species']
        pet.breed = request.POST.get('breed', '')
        pet.age = request.POST['age']
        pet.sex = request.POST['sex']
        pet.size = request.POST['size']
        pet.color = request.POST['color']
        pet.vaccination_status = request.POST.get('vaccination_status') == 'on'
        pet.spay_neuter_status = request.POST.get('spay_neuter_status') == 'on'
        pet.medical_notes = request.POST.get('medical_notes', '')
        pet.status = request.POST['status']
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


# Medical Record Views
@login_required
def medical_add(request, pet_id):
    pet = get_object_or_404(Pet, pet_id=pet_id)
    if request.method == 'POST':
        MedicalRecord.objects.create(
            pet=pet,
            vet=request.POST.get('vet_id') and Veterinary.objects.get(pk=request.POST.get('vet_id')) or None,
            visit_date=request.POST['visit_date'],
            diagnosis=request.POST['diagnosis'],
            treatment=request.POST['treatment'],
            weight=request.POST.get('weight') or None,
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Medical record added successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    vets = Veterinary.objects.all()
    return render(request, 'animals/medical_form.html', {'pet': pet, 'vets': vets})


@login_required
def medical_delete(request, pk):
    record = get_object_or_404(MedicalRecord, medical_id=pk)
    pet_id = record.pet.pet_id
    record.delete()
    messages.success(request, 'Medical record deleted!')
    return redirect('pet_detail', pk=pet_id)


# Vaccination Views
@login_required
def vaccination_add(request, pet_id):
    pet = get_object_or_404(Pet, pet_id=pet_id)
    if request.method == 'POST':
        Vaccination.objects.create(
            pet=pet,
            vet=request.POST.get('vet_id') and Veterinary.objects.get(pk=request.POST.get('vet_id')) or None,
            vaccine_name=request.POST['vaccine_name'],
            dose_no=request.POST['dose_no'],
            vaccination_date=request.POST['vaccination_date'],
            next_due_date=request.POST['next_due_date'],
        )
        # Update pet vaccination status
        pet.vaccination_status = True
        pet.save()
        messages.success(request, 'Vaccination record added successfully!')
        return redirect('pet_detail', pk=pet.pet_id)

    vets = Veterinary.objects.all()
    return render(request, 'animals/vaccination_form.html', {'pet': pet, 'vets': vets})


@login_required
def vaccination_delete(request, pk):
    vacc = get_object_or_404(Vaccination, vaccination_id=pk)
    pet_id = vacc.pet.pet_id
    vacc.delete()
    messages.success(request, 'Vaccination record deleted!')
    return redirect('pet_detail', pk=pet_id)


# Veterinary Views
@login_required
def vet_list(request):
    vets = Veterinary.objects.all()
    return render(request, 'animals/vet_list.html', {'vets': vets})


@login_required
def vet_add(request):
    if request.method == 'POST':
        Veterinary.objects.create(
            full_name=request.POST['full_name'],
            clinic_name=request.POST['clinic_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            license_no=request.POST['license_no'],
        )
        messages.success(request, 'Veterinarian added successfully!')
        return redirect('vet_list')
    return render(request, 'animals/vet_form.html')


@login_required
def vet_delete(request, pk):
    vet = get_object_or_404(Veterinary, vet_id=pk)
    vet.delete()
    messages.success(request, 'Veterinarian deleted!')
    return redirect('vet_list')