from django.db import models
from apps.animals.models import Pet
from apps.accounts.models import Staff

class ShelterBranch(models.Model):
    shelter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class KennelCage(models.Model):
    TYPE_CHOICES = [('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Quarantine', 'Quarantine')]
    STATUS_CHOICES = [('Available', 'Available'), ('Occupied', 'Occupied'), ('Maintenance', 'Maintenance')]

    kennel_id = models.AutoField(primary_key=True)
    shelter = models.ForeignKey(ShelterBranch, on_delete=models.CASCADE, related_name='kennels')
    kennel_code = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.kennel_code} - {self.shelter.name}"

class IntakeRecord(models.Model):
    INTAKE_TYPES = [('Stray', 'Stray'), ('Owner Surrender', 'Owner Surrender'),
                    ('Transfer', 'Transfer'), ('Rescue', 'Rescue')]

    intake_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='intake_records')
    shelter = models.ForeignKey(ShelterBranch, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    intake_type = models.CharField(max_length=50, choices=INTAKE_TYPES)
    intake_date = models.DateField(auto_now_add=True)
    condition_notes = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Intake {self.intake_type} - {self.pet.name} on {self.intake_date}"