from django.db import models
from django.core.exceptions import ValidationError
from apps.animals.models import Pet
from apps.accounts.models import Staff


class ShelterBranch(models.Model):
    shelter_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'shelter_branches'

    def __str__(self):
        return self.name


class KennelCage(models.Model):
    TYPE_CHOICES = [('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Quarantine', 'Quarantine')]
    STATUS_CHOICES = [('Available', 'Available'), ('Occupied', 'Occupied'), ('Maintenance', 'Maintenance')]

    kennel_id = models.AutoField(primary_key=True)
    shelter = models.ForeignKey(ShelterBranch, on_delete=models.CASCADE, related_name='kennels')
    kennel_code = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    class Meta:
        db_table = 'kennel_cages'
        unique_together = ['shelter', 'kennel_code']

    def clean(self):
        if self.current_occupancy > self.capacity:
            raise ValidationError('Current occupancy cannot exceed capacity.')


class IntakeRecord(models.Model):
    INTAKE_TYPES = [('Stray', 'Stray'), ('Surrender', 'Surrender'), ('Rescue', 'Rescue')]

    intake_id = models.AutoField(primary_key=True)
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='intake_record')
    shelter = models.ForeignKey(ShelterBranch, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    intake_type = models.CharField(max_length=50, choices=INTAKE_TYPES)
    intake_date = models.DateField(auto_now_add=True)
    condition_notes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'intake_records'