from django.db import models

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name_plural = '1. Contact'