from django.db import models
from django.core.exceptions import ValidationError
from apps.animals.models import Pet


class FosterAssignment(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    foster_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='foster_assignments')
    foster_name = models.CharField(max_length=200)
    foster_phone = models.CharField(max_length=20)
    foster_address = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    class Meta:
        db_table = 'foster_assignments'

    def __str__(self):
        return f"{self.pet.name} fostered by {self.foster_name}"

    def clean(self):
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError('End date must be after start date.')

    def save(self, *args, **kwargs):
        if self.status == 'Active':
            existing = FosterAssignment.objects.filter(
                pet=self.pet,
                status='Active'
            ).exclude(foster_id=self.foster_id if self.foster_id else None)
            if existing.exists():
                raise ValidationError('This pet already has an active foster assignment.')
        super().save(*args, **kwargs)