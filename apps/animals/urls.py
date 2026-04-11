from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('add/', views.pet_add, name='pet_add'),
    path('<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/edit/', views.pet_edit, name='pet_edit'),
    path('<int:pk>/delete/', views.pet_delete, name='pet_delete'),
]