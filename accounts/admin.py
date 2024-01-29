
from django.contrib import admin                                                                          # Importing the admin module from django.contrib
from accounts.models import *                                                                              # Importing all models from the accounts app


# Registering the User model with the admin site
@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
    list_display = ('username', 'first_name', 'last_name', 'email')                                              # Specifying the fields to be displayed in the admin list view for User model


# Registering the Doctor model with the admin site
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'qualification', 'service_type', 'nmc_number', 'status')       # Specify the fields to be displayed in the admin list view for Doctor model
    list_filter = ('status',)                                                                                  # Add a filter for the 'status' field in the admin list view
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')                   # Add search functionality for specific fields in the admin list view


# Registering the Operator model with the admin site
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'address')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name') 


# Registering the Pet Owner model with the admin site
@admin.register(PetOwner)
class PetOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'mobile', 'address')
    search_fields = ('first_name', 'last_name', 'user__username', 'user__email') 