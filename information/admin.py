from django.contrib import admin
from information.models import *
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',  'phone')
    search_fields = ('first_name', 'last_name',  'phone')