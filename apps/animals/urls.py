from django.urls import path
from . import views

urlpatterns = [
    # Pet URLs
    path('', views.pet_list, name='pet_list'),
    path('add/', views.pet_add, name='pet_add'),
    path('<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/edit/', views.pet_edit, name='pet_edit'),
    path('<int:pk>/delete/', views.pet_delete, name='pet_delete'),

    # Quick Add Medical Record for Vets
    path('medical-record/add/', views.add_medical_record_quick, name='add_medical_record_quick'),

    # Quarantine URLs
    path('quarantine-list/', views.quarantine_list, name='quarantine_list'),
    path('quarantine-dashboard/', views.quarantine_dashboard, name='quarantine_dashboard'),
    path('quarantine/<int:pk>/', views.quarantine_pet, name='quarantine_pet'),
    path('quarantine/release/<int:pk>/', views.release_from_quarantine, name='release_quarantine'),

    # Medical Record URLs
    path('<int:pet_id>/medical/add/', views.medical_add, name='medical_add'),
    path('medical/<int:pk>/delete/', views.medical_delete, name='medical_delete'),
    path('medical-records/', views.medical_record_list, name='medical_record_list'),

    # Vaccination URLs
    path('<int:pet_id>/vaccination/add/', views.vaccination_add, name='vaccination_add'),
    path('vaccination/<int:pk>/delete/', views.vaccination_delete, name='vaccination_delete'),
    path('vaccination-reminders/', views.vaccination_reminders, name='vaccination_reminders'),
    path('vaccination/<int:pk>/complete/', views.mark_vaccination_completed, name='mark_vaccination_completed'),

    # Veterinary URLs
    path('vets/', views.vet_list, name='vet_list'),
    path('vets/add/', views.vet_add, name='vet_add'),
    path('vets/<int:pk>/delete/', views.vet_delete, name='vet_delete'),

    # Medical Statistics URLs
    path('medical-stats/', views.medical_statistics, name='medical_statistics'),
    path('<int:pk>/medical-summary/', views.pet_medical_summary, name='pet_medical_summary'),
    path('<int:pk>/export-medical/', views.export_medical_records, name='export_medical_records'),
    path('bulk-import/', views.bulk_import_pets, name='bulk_import_pets'),
]