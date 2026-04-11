from django.contrib import admin
from .models import ShelterBranch, KennelCage, IntakeRecord

admin.site.register(ShelterBranch)
admin.site.register(KennelCage)
admin.site.register(IntakeRecord)