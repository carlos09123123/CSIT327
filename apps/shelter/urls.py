from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shelter_index'),
    # ShelterBranch URLs
    path('branches/', views.ShelterBranchListView.as_view(), name='branch_list'),
    path('branches/add/', views.ShelterBranchCreateView.as_view(), name='branch_add'),
    path('branches/<int:pk>/edit/', views.ShelterBranchUpdateView.as_view(), name='branch_edit'),
    path('branches/<int:pk>/delete/', views.ShelterBranchDeleteView.as_view(), name='branch_delete'),
    # KennelCage URLs
    path('kennels/', views.KennelCageListView.as_view(), name='kennel_list'),
    path('kennels/add/', views.KennelCageCreateView.as_view(), name='kennel_add'),
    path('kennels/<int:pk>/edit/', views.KennelCageUpdateView.as_view(), name='kennel_edit'),
    path('kennels/<int:pk>/delete/', views.KennelCageDeleteView.as_view(), name='kennel_delete'),
    # IntakeRecord URLs
    path('intakes/', views.IntakeRecordListView.as_view(), name='intake_list'),
    path('intakes/add/', views.IntakeRecordCreateView.as_view(), name='intake_add'),
    path('intakes/<int:pk>/edit/', views.IntakeRecordUpdateView.as_view(), name='intake_edit'),
    path('intakes/<int:pk>/delete/', views.IntakeRecordDeleteView.as_view(), name='intake_delete'),
]