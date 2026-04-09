from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fostering_index'),
    path('assignments/', views.FosterAssignmentListView.as_view(), name='assignment_list'),
    path('assignments/add/', views.FosterAssignmentCreateView.as_view(), name='assignment_add'),
    path('assignments/<int:pk>/edit/', views.FosterAssignmentUpdateView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.FosterAssignmentDeleteView.as_view(), name='assignment_delete'),
]