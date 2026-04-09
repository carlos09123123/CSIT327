from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Veterinary(models.Model):
    vet_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    license_no = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Dr. {self.full_name} - {self.clinic_name}"

    def get_absolute_url(self):
        return reverse('vet_list')


class Pet(models.Model):
    SPECIES_CHOICES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Bird', 'Bird'), ('Rabbit', 'Rabbit'), ('Other', 'Other')]
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    SIZE_CHOICES = [('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')]
    STATUS_CHOICES = [('Available', 'Available'), ('Pending', 'Pending'), ('Adopted', 'Adopted'),
                      ('Fostered', 'Fostered'), ('Medical', 'Medical'), ('Quarantine', 'Quarantine')]

    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], help_text="Age in months")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    vaccination_status = models.BooleanField(default=False)
    spay_neuter_status = models.BooleanField(default=False)
    medical_notes = models.TextField(blank=True)
    intake_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.species}, {self.age} months)"

    def get_absolute_url(self):
        return reverse('pet_detail', args=[str(self.pet_id)])


class MedicalRecord(models.Model):
    medical_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    vet = models.ForeignKey(Veterinary, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Medical Record: {self.pet.name} - {self.visit_date}"


class Vaccination(models.Model):
    vaccination_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccinations')
    vet = models.ForeignKey(Veterinary, on_delete=models.SET_NULL, null=True)
    vaccine_name = models.CharField(max_length=100)
    dose_no = models.IntegerField()
    vaccination_date = models.DateField()
    next_due_date = models.DateField()

    def __str__(self):
        return f"{self.vaccine_name} - Dose {self.dose_no} for {self.pet.name}"