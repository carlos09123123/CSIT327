from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from apps.animals.models import Pet
from apps.accounts.models import Staff


class Adopter(models.Model):
    adopter_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=100, blank=True, null=True)
    has_other_pets = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'adopters'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_authenticated(self):
        return True

    def clean(self):
        if self.date_of_birth:
            today = timezone.now().date()
            age = today.year - self.date_of_birth.year
            if age < 18:
                raise ValidationError('Adopter must be at least 18 years old.')

    def can_submit_application(self):
        return self.applications.filter(status='Pending').count() < 3

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    application_id = models.AutoField(primary_key=True)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE, related_name='applications')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    interview_schedule = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'adoption_applications'

    def __str__(self):
        return f"Application for {self.pet.name} by {self.adopter.first_name}"

    def clean(self):
        if self.pet.status != 'Available':
            raise ValidationError('Pet must be available for adoption.')
        if not self.adopter.can_submit_application():
            raise ValidationError('Adopter already has 3 pending applications.')


class Interview(models.Model):
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    ]

    interview_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, related_name='interviews')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    interview_datetime = models.DateTimeField()
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'interviews'

    def __str__(self):
        return f"Interview for Application #{self.application.application_id}"


class HomeVisit(models.Model):
    RESULT_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    ]

    visit_id = models.AutoField(primary_key=True)
    application = models.ForeignKey(AdoptionApplication, on_delete=models.CASCADE, related_name='home_visits')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'home_visits'

    def __str__(self):
        return f"Home Visit for Application #{self.application.application_id}"


class Adoption(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    adoption_id = models.AutoField(primary_key=True)
    application = models.OneToOneField(AdoptionApplication, on_delete=models.CASCADE, related_name='adoption')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoptions')
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE, related_name='adoptions')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    adoption_date = models.DateField()
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')

    class Meta:
        db_table = 'adoptions'

    def __str__(self):
        return f"Adoption of {self.pet.name} by {self.adopter.first_name}"

    def clean(self):
        if self.application.status != 'Approved':
            raise ValidationError('Application must be approved before adoption.')


class Payment(models.Model):
    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('GCash', 'GCash'),
        ('Card', 'Card'),
    ]
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Refunded', 'Refunded'),
    ]

    payment_id = models.AutoField(primary_key=True)
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_no = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"Payment of ${self.amount} for Adoption #{self.adoption.adoption_id}"

    def clean(self):
        if self.amount != self.adoption.adoption_fee:
            raise ValidationError('Payment amount must match the adoption fee.')