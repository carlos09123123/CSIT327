from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fostering_index'),

    # Foster URLs
    path('fosters/', views.foster_list, name='foster_list'),
    path('fosters/add/', views.foster_add, name='foster_add'),
    path('fosters/<int:pk>/', views.foster_detail, name='foster_detail'),
    path('fosters/<int:pk>/edit/', views.foster_edit, name='foster_edit'),
    path('fosters/<int:pk>/delete/', views.foster_delete, name='foster_delete'),

    # Application URLs
    path('applications/', views.application_list, name='application_list'),
    path('applications/add/', views.application_add, name='application_add'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/edit/', views.application_edit, name='application_edit'),
    path('applications/<int:pk>/delete/', views.application_delete, name='application_delete'),

    # Assignment URLs
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/add/', views.assignment_add, name='assignment_add'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/edit/', views.assignment_edit, name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),

    # Check-in URLs
    path('assignments/<int:assignment_id>/checkin/add/', views.checkin_add, name='checkin_add'),
    path('checkins/<int:pk>/edit/', views.checkin_edit, name='checkin_edit'),
    path('checkins/<int:pk>/delete/', views.checkin_delete, name='checkin_delete'),
]