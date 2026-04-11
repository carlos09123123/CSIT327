from django.urls import path
from . import views

urlpatterns = [
    # Public registration
    path('register/', views.adopter_register, name='adopter_register'),

    # Adopter dashboard and actions
    path('dashboard/', views.adopter_dashboard, name='adopter_dashboard'),
    path('apply/<int:pet_id>/', views.adopter_apply, name='adopter_apply'),
    path('apply-list/', views.adopter_apply_list, name='adopter_apply_list'),

    # Adoption Management
    path('', views.adoption_list, name='adoption_list'),
    path('add/', views.adoption_add, name='adoption_add'),
    path('edit/<int:pk>/', views.adoption_edit, name='adoption_edit'),
    path('delete/<int:pk>/', views.adoption_delete, name='adoption_delete'),

    # Application Management
    path('applications/', views.application_list, name='application_list'),
    path('applications/add/', views.application_add, name='application_add'),
    path('applications/approve/<int:pk>/', views.application_approve, name='application_approve'),
    path('applications/reject/<int:pk>/', views.application_reject, name='application_reject'),

    # Interview Management
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/add/<int:application_id>/', views.interview_add, name='interview_add'),
    path('interviews/result/<int:pk>/', views.interview_result, name='interview_result'),  # ADD THIS

    # Home Visit Management
    path('homevisits/', views.homevisit_list, name='homevisit_list'),
    path('homevisits/add/<int:application_id>/', views.homevisit_add, name='homevisit_add'),
    path('homevisits/result/<int:pk>/', views.homevisit_result, name='homevisit_result'),  # ADD THIS

    # Payment Management
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/<int:adoption_id>/', views.payment_add, name='payment_add'),
]