from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import connection, IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from .models import UserProfile
from django.urls import reverse


def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def service_view(request):
    return render(request, 'service.html')

def team_view(request):
    return render(request, 'team.html')

def contact_view(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        phone = request.POST['phone']
        notes = request.POST['notes']

        query = "INSERT INTO contact_details (first_name, last_name, email, phone, notes) values (%s, %s, %s, %s, %s)"
        val = (first_name, last_name, email, phone, notes)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, val)
                connection.commit()
            return HttpResponseRedirect(request.path)
        except IntegrityError:
            return HttpResponse("Something went wrong")
    return render(request, 'contact.html')

def booking_view(request):
    if request.user.is_authenticated:
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
            purposeOfVisit = request.POST['visit']
            symptonOfDisease = request.POST['symptoms']
            methodOfTreatment = request.POST['method']
            city = request.POST['city']
            tole = request.POST['page']
            houseNumber = request.POST['house_number']
            date = request.POST['bdate']
            time = request.POST['btime']

            query = "INSERT INTO booking_details (email, phone, address, pet_name, breed, age, color, gender, disease, ongoing_medication, purpose_of_visit, symptom, method, city, tole, house_number, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (email, phone, address, petname, breed, age, color, gender, nameOfDisease, onGoingMedication, purposeOfVisit, symptonOfDisease, methodOfTreatment, city, tole, houseNumber, date, time)

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, val)
                    connection.commit()
                return HttpResponseRedirect('/booking')
            except IntegrityError:
                return HttpResponse("Something went wrong")
    else:
        return redirect('login')
    
    return render(request, 'booking.html')

def password_view(request):
    return render(request, 'password.html')

def passwordreset_view(request):
    return render(request, 'passwordreset.html')

def faq_view(request):
    return render(request, 'faq.html')

def feedback_view(request):
    return render(request, 'feedback.html')

def terms_view(request):
    return render(request, 'terms.html')

def payment_view(request):
    return render(request, 'payment.html')




def adminnav_view(request):
    return render(request, 'admin_nav.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_app_view(request):
    return render(request, 'admin_app.html')

def admin_doctor_view(request):
    return render(request, 'admin_doctor.html')

def admin_patient_view(request):
    return render(request, 'admin_patient.html')

def admin_payment_view(request):
    return render(request, 'admin_payment.html')





def usernav_view(request):
    return render(request, 'user_nav.html')

def uhistory_view(request):
    return render(request, 'user_history.html')

def userdashboard_view(request):
    return render(request, 'user_dashboard.html')

def userapp_view(request):
    return render(request, 'user_app.html')

def userpayment_view(request):
    return render(request, 'user_payment.html')

def userprofile_view(request):
    return render(request, 'user_profile.html')



def doctordashmain_view(request):
    return render(request, 'doctordash_main.html')

def doctorpatient_view(request):
    return render(request, 'doctor_patient.html')

def doctorprofile_view(request):
    return render(request, 'doctor_profile.html')

def doctorapp_view(request):
    return render(request, 'doctorapp.html')

def doctornav_view(request):
    return render(request, 'doctornav.html')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def doc_register_view(request):
    return render(request, 'doc_register.html')

def login_view(request):
    if request.method == 'POST':
        getEmail = request.POST['login-email']
        getPassword = request.POST['login-password']
        user = authenticate(request, username=getEmail, password=getPassword)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/user_dashboard')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['reg-first-name']
            last_name = request.POST['reg-last-name']
            email = request.POST['reg-email']
            phone = request.POST['reg-phone']
            gender = request.POST.get('reg-gender')
            password = request.POST['reg-password']
            address = request.POST['reg-address']
            
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)

            query = "INSERT INTO pet_owner (first_name, last_name, email, phone_number, gender, address) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (first_name, last_name, email, phone, gender, address)

            with connection.cursor() as cursor:
                cursor.execute(query, val)
                connection.commit()

            user_profile = UserProfile(user=user, phone_number=phone, gender=gender, address=address)

            user_profile.save()

            return redirect('login')

        except MultiValueDictKeyError as e:
            return render(request, 'register.html', {'error_message': f'Missing key: {e}'})
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')