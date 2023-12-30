from django.db import models
from accounts.models import User, Doctor, PetOwner
import uuid
# Create your models here.

class Time(models.Model):
    start_time = models.TimeField(default=None, null=True, blank=True)
    end_time = models.TimeField(default=None, null=True, blank=True)
    duration = models.IntegerField(default=None, null=True, blank=True)

    available_daytimes = models.TextField(null=True, blank=True, default='')
    occupied_daytimes = models.TextField(null=True, blank=True, default='')
    status = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

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
    purchase_id =  models.UUIDField(max_length=150, unique=True, default=uuid.uuid4)
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
    time = models.ForeignKey(Time, on_delete=models.CASCADE, null=True, blank=True, default=None)

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


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete = models.CASCADE)
    payment_method = models.CharField(max_length=255, choices=[('Khalti', 'Khalti')])
    payment_completed = models.BooleanField(default = False, null=True, blank=True)

    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booking.user.first_name} {self.booking.user.last_name}'

    class Meta:
        verbose_name_plural = '3. Payment'