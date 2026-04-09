from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import FosterAssignment
from django.contrib import messages


@login_required
def index(request):
    return render(request, 'fostering/index.html')


class FosterAssignmentListView(ListView):
    model = FosterAssignment
    template_name = 'fostering/assignment_list.html'
    context_object_name = 'assignments'


class FosterAssignmentCreateView(CreateView):
    model = FosterAssignment
    template_name = 'fostering/assignment_form.html'
    fields = ['pet', 'foster_name', 'foster_phone', 'foster_address', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('assignment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Foster assignment added successfully!')
        return super().form_valid(form)


class FosterAssignmentUpdateView(UpdateView):
    model = FosterAssignment
    template_name = 'fostering/assignment_form.html'
    fields = ['pet', 'foster_name', 'foster_phone', 'foster_address', 'start_date', 'end_date', 'status']
    success_url = reverse_lazy('assignment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Foster assignment updated successfully!')
        return super().form_valid(form)


class FosterAssignmentDeleteView(DeleteView):
    model = FosterAssignment
    template_name = 'fostering/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Foster assignment deleted successfully!')
        return super().delete(request, *args, **kwargs)
