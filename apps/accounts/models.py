from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


class Staff(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Vet', 'Veterinarian'),
        ('Staff', 'Staff'),
        ('Volunteer', 'Volunteer'),
    ]

    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"