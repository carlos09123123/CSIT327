from django.db import models
from apps.animals.models import Pet

class FosterAssignment(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]

    foster_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='foster_assignments')
    foster_name = models.CharField(max_length=200)
    foster_phone = models.CharField(max_length=20)
    foster_address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.pet.name} fostered by {self.foster_name}"

    @property
    def is_active(self):
        return self.status == 'Active'