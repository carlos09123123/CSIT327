from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fostering_index'),
]