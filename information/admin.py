from django.contrib import admin
from information.models import *
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',  'phone')                                      #specifies which fields of the model should be displayed in the list view of the model in the Django admin interface
    search_fields = ('first_name', 'last_name',  'phone')                                    # specifies which fields of the model should be searchable in the Django admin interface

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email',  'details')