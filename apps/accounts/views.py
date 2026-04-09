from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Staff


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})


@login_required
def staff_index(request):
    return render(request, 'accounts/staff_list.html', {'staffs': Staff.objects.all()})


class StaffListView(ListView):
    model = Staff
    template_name = 'accounts/staff_list.html'
    context_object_name = 'staffs'


class StaffCreateView(CreateView):
    model = Staff
    template_name = 'accounts/staff_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'status']
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        staff = form.save(commit=False)
        staff.set_password('defaultpassword')
        staff.save()
        messages.success(self.request, 'Staff added successfully!')
        return super().form_valid(form)


class StaffUpdateView(UpdateView):
    model = Staff
    template_name = 'accounts/staff_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'status']
    success_url = reverse_lazy('staff_list')

    def form_valid(self, form):
        messages.success(self.request, 'Staff updated successfully!')
        return super().form_valid(form)


class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'accounts/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Staff deleted successfully!')
        return super().delete(request, *args, **kwargs)
