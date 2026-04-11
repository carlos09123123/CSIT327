from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff

class StaffAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'status')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (('Shelter Info', {'fields': ('role', 'phone', 'status')}),)

admin.site.register(Staff, StaffAdmin)