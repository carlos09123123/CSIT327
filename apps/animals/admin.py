from django.contrib import admin
from .models import Pet, MedicalRecord, Vaccination, Veterinary

admin.site.register(Pet)
admin.site.register(MedicalRecord)
admin.site.register(Vaccination)
admin.site.register(Veterinary)