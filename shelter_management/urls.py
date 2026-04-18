from django.contrib import admin
from django.urls import path, include
from apps.accounts import views  # Note: 'apps.accounts' because apps are in apps folder
from apps.fostering import views as fostering_views  # Import fostering views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fostering_views.index, name='index'),  # Change made here
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Include app URLs - with 'apps.' prefix
    path('animals/', include('apps.animals.urls')),
    path('shelter/', include('apps.shelter.urls')),
    path('fostering/', include('apps.fostering.urls')),
    path('adoptions/', include('apps.adoptions.urls')),
    path('accounts/', include('apps.accounts.urls')),
]