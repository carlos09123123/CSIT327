from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ShelterBranch, KennelCage, IntakeRecord
from django.contrib import messages


@login_required
def index(request):
    return render(request, 'shelter/index.html')


# ShelterBranch Views
class ShelterBranchListView(ListView):
    model = ShelterBranch
    template_name = 'shelter/branch_list.html'
    context_object_name = 'branches'


class ShelterBranchCreateView(CreateView):
    model = ShelterBranch
    template_name = 'shelter/branch_form.html'
    fields = ['name', 'address', 'city', 'contact_number', 'email']
    success_url = reverse_lazy('branch_list')

    def form_valid(self, form):
        messages.success(self.request, 'Shelter branch added successfully!')
        return super().form_valid(form)


class ShelterBranchUpdateView(UpdateView):
    model = ShelterBranch
    template_name = 'shelter/branch_form.html'
    fields = ['name', 'address', 'city', 'contact_number', 'email']
    success_url = reverse_lazy('branch_list')

    def form_valid(self, form):
        messages.success(self.request, 'Shelter branch updated successfully!')
        return super().form_valid(form)


class ShelterBranchDeleteView(DeleteView):
    model = ShelterBranch
    template_name = 'shelter/branch_confirm_delete.html'
    success_url = reverse_lazy('branch_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Shelter branch deleted successfully!')
        return super().delete(request, *args, **kwargs)


# KennelCage Views
class KennelCageListView(ListView):
    model = KennelCage
    template_name = 'shelter/kennel_list.html'
    context_object_name = 'kennels'


class KennelCageCreateView(CreateView):
    model = KennelCage
    template_name = 'shelter/kennel_form.html'
    fields = ['shelter', 'kennel_code', 'type', 'capacity', 'status']
    success_url = reverse_lazy('kennel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Kennel added successfully!')
        return super().form_valid(form)


class KennelCageUpdateView(UpdateView):
    model = KennelCage
    template_name = 'shelter/kennel_form.html'
    fields = ['shelter', 'kennel_code', 'type', 'capacity', 'status']
    success_url = reverse_lazy('kennel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Kennel updated successfully!')
        return super().form_valid(form)


class KennelCageDeleteView(DeleteView):
    model = KennelCage
    template_name = 'shelter/kennel_confirm_delete.html'
    success_url = reverse_lazy('kennel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Kennel deleted successfully!')
        return super().delete(request, *args, **kwargs)


# IntakeRecord Views
class IntakeRecordListView(ListView):
    model = IntakeRecord
    template_name = 'shelter/intake_list.html'
    context_object_name = 'intakes'


class IntakeRecordCreateView(CreateView):
    model = IntakeRecord
    template_name = 'shelter/intake_form.html'
    fields = ['pet', 'shelter', 'staff', 'intake_type', 'condition_notes', 'notes']
    success_url = reverse_lazy('intake_list')

    def form_valid(self, form):
        messages.success(self.request, 'Intake record added successfully!')
        return super().form_valid(form)


class IntakeRecordUpdateView(UpdateView):
    model = IntakeRecord
    template_name = 'shelter/intake_form.html'
    fields = ['pet', 'shelter', 'staff', 'intake_type', 'condition_notes', 'notes']
    success_url = reverse_lazy('intake_list')

    def form_valid(self, form):
        messages.success(self.request, 'Intake record updated successfully!')
        return super().form_valid(form)


class IntakeRecordDeleteView(DeleteView):
    model = IntakeRecord
    template_name = 'shelter/intake_confirm_delete.html'
    success_url = reverse_lazy('intake_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Intake record deleted successfully!')
        return super().delete(request, *args, **kwargs)
