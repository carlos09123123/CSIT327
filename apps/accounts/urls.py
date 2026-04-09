from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_index, name='accounts_index'),
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/add/', views.StaffCreateView.as_view(), name='staff_add'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
]