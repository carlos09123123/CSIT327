from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Staff


class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    phone = forms.CharField(required=False, max_length=20)
    role = forms.ChoiceField(choices=Staff.ROLE_CHOICES, required=True)

    # ========== VETERINARY FIELDS (only shown when role is Vet) ==========
    clinic_name = forms.CharField(required=False, max_length=200, help_text="Required for Veterinarians")
    license_no = forms.CharField(required=False, max_length=50, help_text="Required for Veterinarians")
    is_accredited = forms.BooleanField(required=False, initial=True,
                                       help_text="Accredited to perform medical procedures")

    # =====================================================================

    class Meta:
        model = Staff
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role',
                  'password1', 'password2', 'clinic_name', 'license_no', 'is_accredited')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        clinic_name = cleaned_data.get('clinic_name')
        license_no = cleaned_data.get('license_no')

        # Validate veterinary fields when role is Vet
        if role == 'Vet':
            if not clinic_name:
                self.add_error('clinic_name', 'Clinic name is required for Veterinarians.')
            if not license_no:
                self.add_error('license_no', 'License number is required for Veterinarians.')

        return cleaned_data

    def clean_license_no(self):
        license_no = self.cleaned_data.get('license_no')
        role = self.cleaned_data.get('role')

        if role == 'Vet' and license_no:
            from apps.animals.models import Veterinary
            if Veterinary.objects.filter(license_no=license_no).exists():
                raise forms.ValidationError('This license number is already registered.')
        return license_no

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Staff.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user