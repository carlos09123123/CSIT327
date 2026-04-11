from django.urls import path
from . import views

urlpatterns = [
    # Shelter Branch URLs
    path('', views.shelter_list, name='shelter_list'),
    path('add/', views.shelter_add, name='shelter_add'),
    path('edit/<int:pk>/', views.shelter_edit, name='shelter_edit'),
    path('delete/<int:pk>/', views.shelter_delete, name='shelter_delete'),

    # Kennel/Cage URLs
    path('kennels/', views.kennel_list, name='kennel_list'),
    path('kennels/add/', views.kennel_add, name='kennel_add'),
    path('kennels/edit/<int:pk>/', views.kennel_edit, name='kennel_edit'),
    path('kennels/delete/<int:pk>/', views.kennel_delete, name='kennel_delete'),

    # Intake Record URLs
    path('intakes/', views.intake_list, name='intake_list'),
    path('intakes/add/', views.intake_add, name='intake_add'),
    path('intakes/edit/<int:pk>/', views.intake_edit, name='intake_edit'),
    path('intakes/delete/<int:pk>/', views.intake_delete, name='intake_delete'),
]