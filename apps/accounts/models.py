from django.db import models
from django.contrib.auth.models import AbstractUser


class Staff(AbstractUser):
    ROLE_CHOICES = [('Admin', 'Admin'), ('Manager', 'Manager'),
                    ('Vet', 'Veterinarian'), ('Staff', 'Staff')]

    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)  # Django handles this automatically
    status = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"