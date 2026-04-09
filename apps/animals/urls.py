from django.urls import path
from . import views

urlpatterns = [
    # Pet URLs
    path('', views.pet_list, name='pet_list'),
    path('add/', views.pet_add, name='pet_add'),
    path('<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/edit/', views.pet_edit, name='pet_edit'),
    path('<int:pk>/delete/', views.pet_delete, name='pet_delete'),

    # Medical Record URLs
    path('<int:pet_id>/medical/add/', views.medical_add, name='medical_add'),
    path('medical/<int:pk>/delete/', views.medical_delete, name='medical_delete'),

    # Vaccination URLs
    path('<int:pet_id>/vaccination/add/', views.vaccination_add, name='vaccination_add'),
    path('vaccination/<int:pk>/delete/', views.vaccination_delete, name='vaccination_delete'),

    # Veterinary URLs
    path('vets/', views.vet_list, name='vet_list'),
    path('vets/add/', views.vet_add, name='vet_add'),
    path('vets/<int:pk>/delete/', views.vet_delete, name='vet_delete'),
]