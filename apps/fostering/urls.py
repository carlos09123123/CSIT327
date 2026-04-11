from django.urls import path
from . import views

urlpatterns = [
    path('', views.foster_list, name='foster_list'),
    path('add/', views.foster_add, name='foster_add'),
    path('edit/<int:pk>/', views.foster_edit, name='foster_edit'),
    path('delete/<int:pk>/', views.foster_delete, name='foster_delete'),
    path('end/<int:pk>/', views.foster_end, name='foster_end'),
]