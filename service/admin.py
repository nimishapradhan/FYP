from django.contrib import admin
from service.models import *

# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'details', 'price')
    list_filter = ('status',)
    search_fields = ('title',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ( 'user','phone', 'petname', 'date', 'time', 'doctor', 'status')
    search_fields = ('user','phone', 'petname')
    list_filter = ('status',)

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time','status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'payment_method', 'payment_completed')