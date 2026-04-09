from django.contrib import admin
from .models import Foster, FosterApplication, FosterAssignment, FosterCheckIn

@admin.register(Foster)
class FosterAdmin(admin.ModelAdmin):
    list_display = ('foster_id', 'first_name', 'last_name', 'email', 'phone', 'preferred_species', 'max_pets')
    list_filter = ('preferred_species', 'has_other_pets', 'has_children')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

@admin.register(FosterApplication)
class FosterApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'foster', 'status', 'application_date', 'staff')
    list_filter = ('status', 'application_date')
    search_fields = ('foster__first_name', 'foster__last_name', 'foster__email')
    ordering = ('-application_date',)

@admin.register(FosterAssignment)
class FosterAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'pet', 'foster', 'start_date', 'end_date', 'status', 'staff')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('pet__name', 'foster__first_name', 'foster__last_name')
    ordering = ('-start_date',)

@admin.register(FosterCheckIn)
class FosterCheckInAdmin(admin.ModelAdmin):
    list_display = ('checkin_id', 'assignment', 'checkin_date', 'staff', 'next_checkin_date')
    list_filter = ('checkin_date',)
    search_fields = ('assignment__pet__name', 'assignment__foster__first_name')
    ordering = ('-checkin_date',)
