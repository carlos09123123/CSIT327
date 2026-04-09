from django.contrib import admin
from .models import Pet, MedicalRecord, Vaccination, Veterinary

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'age', 'status', 'intake_date']
    list_filter = ['species', 'status', 'size']
    search_fields = ['name', 'breed']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['pet', 'visit_date', 'diagnosis', 'vet']

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['pet', 'vaccine_name', 'dose_no', 'vaccination_date', 'next_due_date']

@admin.register(Veterinary)
class VeterinaryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'clinic_name', 'phone', 'email']