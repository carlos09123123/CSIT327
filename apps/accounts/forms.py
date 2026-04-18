from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'age', 'sex', 'size', 'color',
                  'vaccination_status', 'spay_neuter_status', 'medical_notes', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-select'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'vaccination_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'spay_neuter_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Pet Name',
            'species': 'Species',
            'breed': 'Breed',
            'age': 'Age (months)',
            'sex': 'Sex',
            'size': 'Size',
            'color': 'Color',
            'vaccination_status': 'Vaccinated',
            'spay_neuter_status': 'Spayed/Neutered',
            'medical_notes': 'Medical Notes',
            'status': 'Status',
        }