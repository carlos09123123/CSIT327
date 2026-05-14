from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from PIL import Image
import os


class Veterinary(models.Model):
    vet_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    clinic_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_no = models.CharField(max_length=50, unique=True)
    is_accredited = models.BooleanField(default=True)

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
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
        ('Quarantine', 'Quarantine'),
        ('Medical', 'Medical'),
        ('Fostered', 'Fostered'),
    ]

    CRITICAL_KEYWORDS = ['critical', 'terminal', 'severe', 'contagious', 'infectious', 'parvo', 'distemper']

    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, help_text="Use either birth_date OR age")
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True,
                              help_text="Age in months (if birth_date not provided)")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    vaccination_status = models.BooleanField(default=False)
    spay_neuter_status = models.BooleanField(default=False)
    medical_notes = models.TextField(blank=True, null=True)
    intake_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    photo = models.ImageField(upload_to='pet_photos/', blank=True, null=True)
    photo_thumbnail = models.ImageField(upload_to='pet_photos/thumbnails/', blank=True, null=True)

    quarantine_start_date = models.DateField(null=True, blank=True)
    quarantine_end_date = models.DateField(null=True, blank=True)
    quarantine_reason = models.TextField(blank=True, null=True)
    quarantine_location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'pets'
        ordering = ['-intake_date']

    def __str__(self):
        return f"{self.name} ({self.species})"

    def save(self, *args, **kwargs):
        if self.photo and not self.photo_thumbnail:
            self.create_thumbnail()
        super().save(*args, **kwargs)

    def create_thumbnail(self):
        try:
            img = Image.open(self.photo.path)
            img.thumbnail((150, 150))
            thumbnail_name = f"thumb_{os.path.basename(self.photo.name)}"
            thumbnail_path = os.path.join('pet_photos/thumbnails/', thumbnail_name)
            img.save(os.path.join(thumbnail_path))
            self.photo_thumbnail = thumbnail_path
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

    def get_age(self):
        if self.birth_date:
            today = date.today()
            years = today.year - self.birth_date.year
            months = today.month - self.birth_date.month
            if months < 0:
                years -= 1
                months += 12
            if years > 0:
                return f"{years} year(s)"
            else:
                return f"{months} month(s)"
        elif self.age:
            return f"{self.age} months"
        return "Unknown"

    @property
    def age_in_months(self):
        if self.birth_date:
            today = date.today()
            return (today.year - self.birth_date.year) * 12 + (today.month - self.birth_date.month)
        return self.age or 0

    def can_be_adopted(self):
        if self.medical_notes:
            notes_lower = self.medical_notes.lower()
            for keyword in self.CRITICAL_KEYWORDS:
                if keyword in notes_lower:
                    return False
        return self.status == 'Available'

    def get_adoption_eligibility_message(self):
        if self.status != 'Available':
            return f"This pet is currently {self.status}. Not available for adoption."
        if self.medical_notes:
            notes_lower = self.medical_notes.lower()
            for keyword in self.CRITICAL_KEYWORDS:
                if keyword in notes_lower:
                    return f"This pet has a critical medical condition ({keyword}). Please consult with veterinarian."
        return "This pet is available for adoption!"

    @property
    def is_quarantined(self):
        return self.status == 'Quarantine'

    @property
    def quarantine_days_left(self):
        if self.quarantine_end_date and self.is_quarantined:
            days_left = (self.quarantine_end_date - date.today()).days
            return max(0, days_left)
        return 0


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
        ordering = ['-visit_date']

    def clean(self):
        if self.visit_date and self.visit_date > timezone.now().date():
            raise ValidationError('Visit date cannot be in the future.')

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
    is_completed = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    class Meta:
        db_table = 'vaccinations'
        ordering = ['-vaccination_date']

    def clean(self):
        if self.next_due_date and self.vaccination_date:
            if self.next_due_date <= self.vaccination_date:
                raise ValidationError('Next due date must be after vaccination date.')

    def __str__(self):
        return f"{self.vaccine_name} - Dose {self.dose_no} for {self.pet.name}"

    @property
    def is_overdue(self):
        return self.next_due_date < date.today() and not self.is_completed

    @property
    def days_until_due(self):
        if self.next_due_date and not self.is_completed:
            days = (self.next_due_date - date.today()).days
            return max(0, days)
        return None