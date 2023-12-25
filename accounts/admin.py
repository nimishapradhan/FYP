from django.contrib import admin
from accounts.models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'qualification', 'service_type', 'nmc_number', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'address')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name') 

@admin.register(PetOwner)
class PetOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'address')
    search_fields = ('first_name', 'last_name', 'user__username', 'user__email') 