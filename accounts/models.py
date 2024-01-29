from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

 # Define a custom User model inheriting from AbstractUser
class User(AbstractUser):
    # first_name last_name email username password is_superuser is_staff is_active date_joined last_login

    # Define boolean fields to represent user roles with default values
    is_admin = models.BooleanField(default = False)
    is_operator = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)
    is_doctor = models.BooleanField(default = False)

    # Define fields for one-time password (OTP) authentication
    otp = models.CharField(max_length=255, default=None, null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now_add = True)
    otp_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = '1. User'                 #specifies the human-readable name for the model in its plural form; when Django refers to the model User in its plural form, it will use '1. User' as the name instead of the default generated name.


# Define a model named Doctor
class Doctor(models.Model):
    # Define a one-to-one relationship with the User model, where each Doctor has one User; when the associated user is deleted it also delete the Doctor instance.
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


# Define a model named PetOwner.
class PetOwner(models.Model):
    # Define a one-to-one relationship with the User model, where each PetOwner is one User;when the associated user is deleted, also delete the PetOwner instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = '3. Pet Owner/ Patient'
    

# Define a model named Operator
class Operator(models.Model):
    # Define a one-to-one relationship with the User model.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = '4. Office Staff / Operator'
