from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    # first_name last_name email username password is_superuser is_staff is_active date_joined last_login
    
    is_admin = models.BooleanField(default = False)
    is_operator = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)
    is_doctor = models.BooleanField(default = False)

    otp = models.CharField(max_length=255, default=None, null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now_add = True)
    otp_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '1. User'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    qualification = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=255, null=True, blank=True)
    nmc_number = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='doctor', null=True, blank=True)

    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = '2. Vet Doctor'


class PetOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = '3. Pet Owner/ Patient'
    

class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = '4. Office Staff / Operator'
