from django.db import models
from apps.animals.models import Pet
from apps.accounts.models import Staff

class Adopter(models.Model):
    adopter_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)
    has_other_pets = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AdoptionApplication(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Under Review', 'Under Review'),
                      ('Approved', 'Approved'), ('Rejected', 'Rejected')]

    application_id = models.AutoField(primary_key=True)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE, related_name='applications')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    interview_schedule = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Application for {self.pet.name} by {self.adopter.first_name}"

class HomeVisit(models.Model):
    RESULT_CHOICES = [('Passed', 'Passed'), ('Failed', 'Failed'), ('Rescheduled', 'Rescheduled')]

    visit_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, related_name='home_visits')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Home Visit for Application #{self.application.application_id}"

class Adoption(models.Model):
    STATUS_CHOICES = [('Completed', 'Completed'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')]

    adoption_id = models.AutoField(primary_key=True)
    application = models.OneToOneField(AdoptionApplication, on_delete=models.CASCADE, related_name='adoption')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoptions')
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE, related_name='adoptions')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    adoption_date = models.DateField()
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')

    def __str__(self):
        return f"Adoption of {self.pet.name} by {self.adopter.first_name}"

class Payment(models.Model):
    METHOD_CHOICES = [('Cash', 'Cash'), ('Credit Card', 'Credit Card'),
                      ('Debit Card', 'Debit Card'), ('Bank Transfer', 'Bank Transfer')]
    STATUS_CHOICES = [('Paid', 'Paid'), ('Pending', 'Pending'), ('Refunded', 'Refunded')]

    payment_id = models.AutoField(primary_key=True)
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_no = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment of ${self.amount} for Adoption #{self.adoption.adoption_id}"