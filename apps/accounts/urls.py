from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_index, name='accounts_index'),
]