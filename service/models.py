from django.db import models
from accounts.models import User, Doctor
# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='services', null=True, blank=True)

    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "1. Services"


class Booking(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    petname = models.CharField(max_length=255, null=True, blank=True)
    breed = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, choices=[(
        'Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    name_of_Disease = models.CharField(max_length=255, null=True, blank=True)
    on_going_medication = models.CharField(
        max_length=255, null=True, blank=True)
    purpose_of_visit = models.CharField(max_length=255, null=True, blank=True)
    symptonm_of_Disease = models.CharField(
        max_length=255, null=True, blank=True)
    booking_type = models.CharField(max_length=255, choices=[(
        'Home', 'Home'), ('Clinic', 'Clinic')], null=True, blank=True, default=None)
    city = models.CharField(max_length=255, null=True, blank=True)
    tole = models.CharField(max_length=255, null=True, blank=True)
    houseNumber = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    booking_status = models.CharField(max_length=255, choices=[('Requested', 'Requested'), ('Confirmed', 'Confirmed'),
                                                               ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')],
                                      default='Requested')

    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = '2. Booking'
