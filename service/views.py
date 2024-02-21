from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from service.models import Service, Booking, Time
from accounts.models import User, Doctor
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date
import uuid
from django.urls import reverse_lazy
from tailtales.settings import MEDIA_URL
# Create your views here.


def service(request):
    service = Service.objects.filter(status = True)
    return render(request, 'service.html', {'service':service, 'MEDIA_URL':MEDIA_URL})

@login_required
def appointment_booking(request):
    if request.user.is_patient:
        service = Service.objects.filter(status = True)
        doctor = Doctor.objects.filter(status = True)
        time= Time.objects.filter(status = True)

        uid = uuid.uuid4()             # generates unique booking id for each booking
        # print(uid)

        return render(request, 'user/user_booking.html', {'service':service, 'doctor':doctor, 'time':time, 'uid':uid})
    else:
        return HttpResponse('Invalid role action')

@login_required
def do_appointment_booking(request):
    if request.user.is_patient:
        if request.method == 'POST':
            email = request.POST['booking_email']
            phone = request.POST['phone']
            address = request.POST['address']
            petname = request.POST['pname']
            breed = request.POST['pbreed']
            age = request.POST['page']
            color = request.POST['pcolor']
            gender = request.POST.get('pgender')
            nameOfDisease = request.POST['pdisease']
            onGoingMedication = request.POST['pmedication']
            symptomOfDisease = request.POST['symptoms']
            booking_type = request.POST['method']
            city = request.POST['city']
            tole = request.POST['page']
            houseNumber = request.POST['house_number']
            date = request.POST['bdate']
            time = request.POST['btime']
            doctor = request.POST['doctor']
            service = request.POST['service']
            user = request.POST['user']
            location = request.POST['location']

            status = False

            bookings = Booking.objects.filter(date=date, time_id=time, doctor_id=doctor).filter(status=True)
            count = bookings.count()

            if count > 0:
                messages.warning(request, 'Already Booked')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            else:
                # booking = Booking(service_id=service, user_id=user, email=email, phone=phone, address=address, petname=petname, breed=breed, 
                #                 age=age, color=color, gender=gender, name_of_Disease = nameOfDisease, on_going_medication = onGoingMedication,
                #                 symptonm_of_Disease=symptomOfDisease, booking_type=booking_type, city=city, tole=tole, houseNumber=houseNumber,
                #                 date=date, time_id=time, doctor_id=doctor, status = 0)
                # booking.save()

                booking = Booking(service_id=service, user_id=user, email=email, phone=phone, address=address, petname=petname, breed=breed, 
                                age=age, color=color, gender=gender, name_of_Disease = nameOfDisease, on_going_medication = onGoingMedication,
                                symptonm_of_Disease=symptomOfDisease, booking_type=booking_type, city=city, tole=tole, houseNumber=houseNumber,
                                date=date, time_id=time, doctor_id=doctor, status=status, location=location)
                
                booking.save()

            return HttpResponseRedirect(reverse_lazy('khalti_request', args=[booking.id]))
    else:
        return HttpResponse('Invalid action role.')
    

