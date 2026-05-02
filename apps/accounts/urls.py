from django.urls import path
from . import views

urlpatterns = [
    # Staff Management (Admin only)
    path('', views.staff_list, name='staff_list'),
    path('register/', views.register_staff, name='register_staff'),
    path('edit/<int:pk>/', views.staff_edit, name='staff_edit'),
    path('delete/<int:pk>/', views.staff_delete, name='staff_delete'),

    # Profile Management (Staff/Admin only)
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('change-password/', views.change_password, name='change_password'),
]