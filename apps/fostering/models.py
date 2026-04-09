from django.db import models
from apps.animals.models import Pet
from apps.accounts.models import Staff

class Foster(models.Model):
    foster_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)
    has_other_pets = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    experience_years = models.IntegerField(default=0, help_text="Years of pet fostering experience")
    preferred_species = models.CharField(max_length=100, blank=True, help_text="Preferred animal species")
    max_pets = models.IntegerField(default=1, help_text="Maximum number of pets they can foster")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FosterApplication(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Under Review', 'Under Review'),
                      ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    application_id = models.AutoField(primary_key=True)
    foster = models.ForeignKey(Foster, on_delete=models.CASCADE, related_name='applications')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    interview_schedule = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Foster Application by {self.foster.first_name} {self.foster.last_name}"

class FosterAssignment(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]

    assignment_id = models.AutoField(primary_key=True)
    foster = models.ForeignKey(Foster, on_delete=models.CASCADE, related_name='assignments')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='foster_assignments')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pet.name} fostered by {self.foster.first_name} {self.foster.last_name}"

    @property
    def is_active(self):
        return self.status == 'Active'

class FosterCheckIn(models.Model):
    checkin_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(FosterAssignment, on_delete=models.CASCADE, related_name='checkins')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    checkin_date = models.DateField()
    pet_condition = models.TextField()
    foster_feedback = models.TextField(blank=True)
    issues = models.TextField(blank=True)
    next_checkin_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Check-in for {self.assignment.pet.name} on {self.checkin_date}"
