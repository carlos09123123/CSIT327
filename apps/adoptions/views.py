from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Adopter, AdoptionApplication, HomeVisit, Adoption, Payment
from apps.animals.models import Pet
from apps.accounts.models import Staff


@login_required
def index(request):
    return render(request, 'adoptions/index.html')


# Adopter Views
class AdopterListView(ListView):
    model = Adopter
    template_name = 'adoptions/adopter_list.html'
    context_object_name = 'adopters'


class AdopterCreateView(CreateView):
    model = Adopter
    template_name = 'adoptions/adopter_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'occupation', 'has_other_pets', 'has_children']
    success_url = reverse_lazy('adopter_list')

    def form_valid(self, form):
        messages.success(self.request, 'Adopter added successfully!')
        return super().form_valid(form)


class AdopterUpdateView(UpdateView):
    model = Adopter
    template_name = 'adoptions/adopter_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'occupation', 'has_other_pets', 'has_children']
    success_url = reverse_lazy('adopter_list')

    def form_valid(self, form):
        messages.success(self.request, 'Adopter updated successfully!')
        return super().form_valid(form)


class AdopterDeleteView(DeleteView):
    model = Adopter
    template_name = 'adoptions/adopter_confirm_delete.html'
    success_url = reverse_lazy('adopter_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Adopter deleted successfully!')
        return super().delete(request, *args, **kwargs)


# AdoptionApplication Views
class AdoptionApplicationListView(ListView):
    model = AdoptionApplication
    template_name = 'adoptions/application_list.html'
    context_object_name = 'applications'


class AdoptionApplicationCreateView(CreateView):
    model = AdoptionApplication
    template_name = 'adoptions/application_form.html'
    fields = ['adopter', 'pet', 'staff', 'status', 'interview_schedule', 'notes']
    success_url = reverse_lazy('application_list')

    def form_valid(self, form):
        messages.success(self.request, 'Application submitted successfully!')
        return super().form_valid(form)


class AdoptionApplicationUpdateView(UpdateView):
    model = AdoptionApplication
    template_name = 'adoptions/application_form.html'
    fields = ['adopter', 'pet', 'staff', 'status', 'interview_schedule', 'notes']
    success_url = reverse_lazy('application_list')

    def form_valid(self, form):
        messages.success(self.request, 'Application updated successfully!')
        return super().form_valid(form)


class AdoptionApplicationDeleteView(DeleteView):
    model = AdoptionApplication
    template_name = 'adoptions/application_confirm_delete.html'
    success_url = reverse_lazy('application_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Application deleted successfully!')
        return super().delete(request, *args, **kwargs)


# HomeVisit Views
class HomeVisitListView(ListView):
    model = HomeVisit
    template_name = 'adoptions/home_visit_list.html'
    context_object_name = 'visits'


class HomeVisitCreateView(CreateView):
    model = HomeVisit
    template_name = 'adoptions/home_visit_form.html'
    fields = ['application', 'staff', 'visit_date', 'result', 'remarks']
    success_url = reverse_lazy('home_visit_list')

    def form_valid(self, form):
        messages.success(self.request, 'Home visit scheduled successfully!')
        return super().form_valid(form)


class HomeVisitUpdateView(UpdateView):
    model = HomeVisit
    template_name = 'adoptions/home_visit_form.html'
    fields = ['application', 'staff', 'visit_date', 'result', 'remarks']
    success_url = reverse_lazy('home_visit_list')

    def form_valid(self, form):
        messages.success(self.request, 'Home visit updated successfully!')
        return super().form_valid(form)


class HomeVisitDeleteView(DeleteView):
    model = HomeVisit
    template_name = 'adoptions/home_visit_confirm_delete.html'
    success_url = reverse_lazy('home_visit_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Home visit deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Adoption Views
class AdoptionListView(ListView):
    model = Adoption
    template_name = 'adoptions/adoption_list.html'
    context_object_name = 'adoptions'


class AdoptionCreateView(CreateView):
    model = Adoption
    template_name = 'adoptions/adoption_form.html'
    fields = ['application', 'adoption_date', 'adoption_fee', 'status']
    success_url = reverse_lazy('adoption_list')

    def form_valid(self, form):
        adoption = form.save(commit=False)
        adoption.pet = form.instance.application.pet
        adoption.adopter = form.instance.application.adopter
        adoption.staff = self.request.user
        adoption.save()
        # Update pet status
        adoption.pet.status = 'Adopted'
        adoption.pet.save()
        messages.success(self.request, 'Adoption completed successfully!')
        return super().form_valid(form)


class AdoptionUpdateView(UpdateView):
    model = Adoption
    template_name = 'adoptions/adoption_form.html'
    fields = ['application', 'adoption_date', 'adoption_fee', 'status']
    success_url = reverse_lazy('adoption_list')

    def form_valid(self, form):
        messages.success(self.request, 'Adoption updated successfully!')
        return super().form_valid(form)


class AdoptionDeleteView(DeleteView):
    model = Adoption
    template_name = 'adoptions/adoption_confirm_delete.html'
    success_url = reverse_lazy('adoption_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Adoption deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Payment Views
class PaymentListView(ListView):
    model = Payment
    template_name = 'adoptions/payment_list.html'
    context_object_name = 'payments'


class PaymentCreateView(CreateView):
    model = Payment
    template_name = 'adoptions/payment_form.html'
    fields = ['adoption', 'amount', 'method', 'reference_no', 'status']
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Payment recorded successfully!')
        return super().form_valid(form)


class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'adoptions/payment_form.html'
    fields = ['adoption', 'amount', 'method', 'reference_no', 'status']
    success_url = reverse_lazy('payment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Payment updated successfully!')
        return super().form_valid(form)


class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'adoptions/payment_confirm_delete.html'
    success_url = reverse_lazy('payment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Payment deleted successfully!')
        return super().delete(request, *args, **kwargs)
