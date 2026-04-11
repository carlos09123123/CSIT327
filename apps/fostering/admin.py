from django.contrib import admin
from .models import FosterAssignment

@admin.register(FosterAssignment)
class FosterAssignmentAdmin(admin.ModelAdmin):
    list_display = ('foster_id', 'pet', 'foster_name', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('pet__name', 'foster_name')