from django.contrib import admin
from django.urls import path, include
from apps.accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.index, name='index'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('animals/', include('apps.animals.urls')),
    path('shelter/', include('apps.shelter.urls')),
    path('fostering/', include('apps.fostering.urls')),
    path('adoptions/', include('apps.adoptions.urls')),
    path('accounts/', include('apps.accounts.urls')),
]