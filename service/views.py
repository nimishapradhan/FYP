from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from service.models import Service, Booking
from accounts.models import User, Doctor
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.

def service(request):
    return render(request, 'service.html')

@login_required
def appointment_booking(request):
    service = Service.objects.filter(status = True)
    doctor = Doctor.objects.filter(status = True)

    return render(request, 'user/user_booking.html', {'service':service, 'doctor':doctor})

@login_required
def do_appointment_booking(request):
    if request.method == 'POST':
        email = request.POST['booking_email']
        phone = request.POST['phone']
        address = request.POST['address']
        petname = request.POST['pname']
        breed = request.POST['pbreed']
        age = request.POST['page']
        color = request.POST['pcolor']
        gender = request.POST['pgender']
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

        booking = Booking(service_id=service, user_id=user, email=email, phone=phone, address=address, petname=petname, breed=breed, 
                          age=age, color=color, gender=gender, name_of_Disease = nameOfDisease, on_going_medication = onGoingMedication,
                          symptonm_of_Disease=symptomOfDisease, booking_type=booking_type, city=city, tole=tole, houseNumber=houseNumber,
                          date=date, time=time, doctor_id=doctor)
        
        booking.save()

        messages.success(request, 'Appointment Booked with Success!!!')
        return redirect('user_appointment_list')