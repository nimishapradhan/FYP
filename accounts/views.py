from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from service.models import Booking
# Create your views here.


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def do_register(request):
    if request.method == 'POST':
        first_name = request.POST['reg-first-name']
        last_name = request.POST['reg-last-name']
        username = request.POST['reg-email']
        mobile = request.POST['reg-phone']
        gender = request.POST.get('reg-gender')
        password = request.POST['reg-password']
        confirm_password = request.POST['reg-confirm-password']
        address = request.POST['reg-address']

        is_patient = True

        for value in [first_name, last_name, username, password, confirm_password]:
            if value is None or value == '':
                messages.success(request, 'Provide all information')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if User.objects.filter(username=username):
            messages.warning(request, 'Email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if password != confirm_password:
            messages.warning(request, 'Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=username, 
                                        is_patient=is_patient)
        user.save()

        pet_owner = PetOwner(user=user, mobile=mobile, gender=gender, address=address)
        pet_owner.save()

        messages.success(request, 'Registration Successful!!!.')
        return redirect('login')
    

def do_login(request):
    if request.method == 'POST':
        username = request.POST['login-email']                           
        password = request.POST['login-password']
        user = auth.authenticate(username=username, password=password)
        
        for value in[username, password]:
            if value is None or value == '':
                messages.warning(request, 'Provide username and password.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user is not None and user.is_patient:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('user_dashboard')
        elif user is not None and user.is_admin:
            auth.login(request, user)
            # messages.success(request, 'Login Successful')
            return HttpResponse("This is admin")
        elif user is not None and user.is_doctor:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('doctor_dashboard')
        elif user is not None and user.is_operator:
            auth.login(request, user)
            # messages.success(request, 'Login Successful')
            return HttpResponse("This is operator")
        else:
            messages.warning(request, 'Username or Password is invalid.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    messages.warning(request, 'Invalid credentials')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out')
    return HttpResponseRedirect('login')


# for pet owner / patient

@login_required
def user_dashboard(request):
    if request.user.is_patient:
        doctor = Doctor.objects.filter(status = True)
        appointment = Booking.objects.filter(user=request.user).filter(status = True).order_by('created_on')[:4]
        return render(request, 'user/user_dashboard.html',{'appointment':appointment, 'doctor':doctor})
    else:
        return HttpResponse('Invalid role')
    
@login_required
def user_appointment_list(request):
    if request.user.is_patient:
        appointment = Booking.objects.filter(user=request.user)
        return render(request, 'user/appointment_history.html', {'appointment':appointment})
    else:
        return HttpResponse('Invalid role')
    
@login_required
def user_payment_list(request):
    if request.user.is_patient:
        return render(request, 'user/payment_history.html')
    else:
        return HttpResponse('Invalid role')
    
@login_required
def user_generate_bill(request):
    if request.user.is_patient:
        return render(request, 'user/generate_bill.html')
    else:
        return HttpResponse('Invalid role')
    
@login_required
def user_profile(request):
    if request.user.is_patient:
        return render(request, 'user/user_profile.html')
    else:
        return HttpResponse('Invalid role')

@login_required
def user_profile_update(request):
    if request.method == 'POST':
        first_name = request.POST['user-first-name']
        last_name = request.POST['user-last-name']
        email = request.POST['user-email']
        username = request.POST['user-email']

        if email != request.user.email and User.objects.filter(email=email):
            messages.warning(request, 'Email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        
        user.save()
        messages.success(request, 'Your profile has been updated.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, 'Invalid Error')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
@login_required
def user_change_password(request):
    if request.method == 'POST':
        old_password = request.POST['current-password']
        new_password = request.POST['new-password']
        confirm_password = request.POST['confirm-password']

        if new_password != confirm_password:
            messages.warning(request, 'Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif old_password == new_password:
            messages.warning(request, 'Old Password and New Password cannot be same.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.get(id=request.user.id)
        # user.password = new_password

        if user.check_password(old_password) == False:
            messages.warning(request, 'Old Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if new_password != request.user.password:
            user.password = make_password(new_password)

        user.save()

        messages.success(request, 'Your password has been changed. Please Login Again.')

        auth.logout(request)
        return redirect('login')


# for doctor ----

@login_required
def doctor_dashboard(request):
    if request.user.is_doctor:
        home_appointments = Booking.objects.filter(doctor=request.user.doctor, status=True, booking_type='home')
        clinic_appointments = Booking.objects.filter(doctor=request.user.doctor, status=True, booking_type='clinic')

        appointments = Booking.objects.filter(doctor=request.user.doctor, status=True).order_by('created_on')[:4]
        totalPatients = appointments.count()
        home = home_appointments.count()
        clinic = clinic_appointments.count()

        return render(request, 'doctor/doctor_dashboard.html', {'appointments': appointments, 'totalPatients':totalPatients, 'home':home, 'clinic':clinic})
    else:
        return HttpResponse('Invalid role action.')
    
@login_required
def doctor_all_appointment(request):
    if request.user.is_doctor:
        appointments = Booking.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor/doctor_all_appointments.html', {"appointments":appointments})
    else:
        return HttpResponse('Invalid role action.')

@login_required
def doctor_single_appointment(request, id):
    if request.user.is_doctor:
        try:
            appointment_detail = Booking.objects.get(doctor=request.user.doctor, id=id)
        except Booking.DoesNotExist:
            return HttpResponse("You do not have permission to access it.")
        
        return render(request, 'doctor/doctor_single_appointment.html', {'app': appointment_detail})
    else:
        return HttpResponse('Invalid role action')
    
@login_required
def doctor_patient_details(request):
    if request.user.is_doctor:
        patient = Booking.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor/doctor_patient_details.html', {'patient':patient})
    else:
        return HttpResponse('Invalid role action')

@login_required
def doctor_single_patient(request, id):
    if request.user.is_doctor:
        try:
            patient_detail = Booking.objects.get(doctor=request.user.doctor, id=id)
        except Booking.DoesNotExist:
            return HttpResponse("You do not have permission to access it.")
        
        return render(request, 'doctor/doctor_single_patient.html', {'patient': patient_detail})
    else:
        return HttpResponse('Invalid role action')
    
@login_required
def doctor_profile(request):
    if request.user.is_doctor:
        return render(request, 'doctor/doctor_profile.html')
    else:
        return HttpResponse('Invalid role action')

@login_required
def doctor_profile_update(request):
    if request.method == 'POST':
        old_password = request.POST['vet-pw']
        new_password = request.POST['new-vet-pw']
        confirm_password = request.POST['confirm-new-vet-pw']

        if new_password != confirm_password:
            messages.warning(request, 'Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif old_password == new_password:
            messages.warning(request, 'Old Password and New Password cannot be same.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.get(id=request.user.id)
        # user.password = new_password

        if user.check_password(old_password) == False:
            messages.warning(request, 'Old Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if new_password != request.user.password:
            user.password = make_password(new_password)

        user.save()

        messages.success(request, 'Your password has been changed. Please Login Again.')

        auth.logout(request)
        return redirect('login')
    

# for admin