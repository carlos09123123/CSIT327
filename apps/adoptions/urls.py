from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='adoptions_index'),
    # Adopter URLs
    path('adopters/', views.AdopterListView.as_view(), name='adopter_list'),
    path('adopters/add/', views.AdopterCreateView.as_view(), name='adopter_add'),
    path('adopters/<int:pk>/edit/', views.AdopterUpdateView.as_view(), name='adopter_edit'),
    path('adopters/<int:pk>/delete/', views.AdopterDeleteView.as_view(), name='adopter_delete'),
    # AdoptionApplication URLs
    path('applications/', views.AdoptionApplicationListView.as_view(), name='application_list'),
    path('applications/add/', views.AdoptionApplicationCreateView.as_view(), name='application_add'),
    path('applications/<int:pk>/edit/', views.AdoptionApplicationUpdateView.as_view(), name='application_edit'),
    path('applications/<int:pk>/delete/', views.AdoptionApplicationDeleteView.as_view(), name='application_delete'),
    # HomeVisit URLs
    path('home-visits/', views.HomeVisitListView.as_view(), name='home_visit_list'),
    path('home-visits/add/', views.HomeVisitCreateView.as_view(), name='home_visit_add'),
    path('home-visits/<int:pk>/edit/', views.HomeVisitUpdateView.as_view(), name='home_visit_edit'),
    path('home-visits/<int:pk>/delete/', views.HomeVisitDeleteView.as_view(), name='home_visit_delete'),
    # Adoption URLs
    path('adoptions/', views.AdoptionListView.as_view(), name='adoption_list'),
    path('adoptions/add/', views.AdoptionCreateView.as_view(), name='adoption_add'),
    path('adoptions/<int:pk>/edit/', views.AdoptionUpdateView.as_view(), name='adoption_edit'),
    path('adoptions/<int:pk>/delete/', views.AdoptionDeleteView.as_view(), name='adoption_delete'),
    # Payment URLs
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payments/add/', views.PaymentCreateView.as_view(), name='payment_add'),
    path('payments/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name='payment_edit'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),
]