from django.contrib import admin
from .models import Adopter, AdoptionApplication, Interview, HomeVisit, Adoption, Payment

@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    list_display = ('adopter_id', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'adopter', 'pet', 'application_date', 'status')
    list_filter = ('status', 'application_date')

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('interview_id', 'application', 'interview_datetime', 'result')
    list_filter = ('result', 'interview_datetime')

@admin.register(HomeVisit)
class HomeVisitAdmin(admin.ModelAdmin):
    list_display = ('visit_id', 'application', 'visit_date', 'result')
    list_filter = ('result', 'visit_date')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('adoption_id', 'pet', 'adopter', 'adoption_date', 'adoption_fee', 'status')
    list_filter = ('status', 'adoption_date')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'adoption', 'amount', 'method', 'payment_date', 'status')
    list_filter = ('method', 'status', 'payment_date')