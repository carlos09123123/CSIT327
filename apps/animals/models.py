from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Veterinary(models.Model):
    vet_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_no = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'veterinary'

    def __str__(self):
        return f"Dr. {self.full_name}"


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('Dog', 'Dog'), ('Cat', 'Cat'), ('Bird', 'Bird'),
        ('Rabbit', 'Rabbit'), ('Other', 'Other')
    ]
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    SIZE_CHOICES = [('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')]
    STATUS_CHOICES = [
        ('Available', 'Available'), ('Pending', 'Pending'), ('Adopted', 'Adopted')
    ]

    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], help_text="Age in months")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    vaccination_status = models.BooleanField(default=False)
    spay_neuter_status = models.BooleanField(default=False)
    medical_notes = models.TextField(blank=True, null=True)
    intake_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    class Meta:
        db_table = 'pets'

    def __str__(self):
        return f"{self.name} ({self.species})"


class MedicalRecord(models.Model):
    medical_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    vet = models.ForeignKey(Veterinary, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'medical_records'

    def clean(self):
        if self.visit_date and self.visit_date > timezone.now().date():
            raise ValidationError('Visit date cannot be in the future.')


class Vaccination(models.Model):
    vaccination_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vet = models.ForeignKey(Veterinary, on_delete=models.SET_NULL, null=True)
    vaccine_name = models.CharField(max_length=100)
    dose_no = models.IntegerField()
    vaccination_date = models.DateField()
    next_due_date = models.DateField()

    class Meta:
        db_table = 'vaccinations'

    def clean(self):
        if self.next_due_date and self.vaccination_date:
            if self.next_due_date <= self.vaccination_date:
                raise ValidationError('Next due date must be after vaccination date.')