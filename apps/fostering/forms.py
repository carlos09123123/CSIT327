from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Adopter


class AdopterRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Adopter
        fields = ['first_name', 'last_name', 'email', 'phone', 'address',
                  'date_of_birth', 'occupation', 'has_other_pets', 'has_children']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError("Passwords do not match.")

        dob = cleaned_data.get('date_of_birth')
        if dob:
            age = timezone.now().date().year - dob.year
            if age < 18:
                raise ValidationError("You must be at least 18 years old.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Adopter.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email