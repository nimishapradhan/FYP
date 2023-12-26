from django.shortcuts import render, redirect
from accounts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from service.models import Booking, Service
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

        if PetOwner.objects.filter(mobile=mobile):
            messages.warning(request, 'Phone number already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if password != confirm_password:
            messages.warning(request, 'Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=username,
                                        is_patient=is_patient)
        user.save()

        pet_owner = PetOwner(user=user, mobile=mobile,
                             gender=gender, address=address)
        pet_owner.save()

        messages.success(request, 'Registration Successful!!!.')
        return redirect('login')


def do_login(request):
    if request.method == 'POST':
        username = request.POST['login-email']
        password = request.POST['login-password']
        user = auth.authenticate(username=username, password=password)

        for value in [username, password]:
            if value is None or value == '':
                messages.warning(request, 'Provide username and password.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if user is not None and user.is_patient:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('user_dashboard')
        elif user is not None and user.is_admin:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
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
        doctor = Doctor.objects.filter(status=True)
        appointment = Booking.objects.filter(user=request.user).filter(
            status=True).order_by('created_on')[:4]
        return render(request, 'user/user_dashboard.html', {'appointment': appointment, 'doctor': doctor})
    else:
        return HttpResponse('Invalid role')


@login_required
def user_appointment_list(request):
    if request.user.is_patient:
        appointment = Booking.objects.filter(user=request.user)
        return render(request, 'user/appointment_history.html', {'appointment': appointment})
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
            messages.warning(
                request, 'Old Password and New Password cannot be same.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.get(id=request.user.id)
        # user.password = new_password

        if user.check_password(old_password) == False:
            messages.warning(request, 'Old Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if new_password != request.user.password:
            user.password = make_password(new_password)

        user.save()

        messages.success(
            request, 'Your password has been changed. Please Login Again.')

        auth.logout(request)
        return redirect('login')


# for doctor ----

@login_required
def doctor_dashboard(request):
    if request.user.is_doctor:
        home_appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True, booking_type='home')
        clinic_appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True, booking_type='clinic')

        appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True).order_by('created_on')[:4]
        totalPatients = appointments.count()
        home = home_appointments.count()
        clinic = clinic_appointments.count()

        return render(request, 'doctor/doctor_dashboard.html', {'appointments': appointments, 'totalPatients': totalPatients, 'home': home, 'clinic': clinic})
    else:
        return HttpResponse('Invalid role action.')


@login_required
def doctor_all_appointment(request):
    if request.user.is_doctor:
        appointments = Booking.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor/doctor_all_appointments.html', {"appointments": appointments})
    else:
        return HttpResponse('Invalid role action.')


@login_required
def doctor_single_appointment(request, id):
    if request.user.is_doctor:
        try:
            appointment_detail = Booking.objects.get(
                doctor=request.user.doctor, id=id)
        except Booking.DoesNotExist:
            return HttpResponse("You do not have permission to access it.")

        return render(request, 'doctor/doctor_single_appointment.html', {'app': appointment_detail})
    else:
        return HttpResponse('Invalid role action')


@login_required
def doctor_patient_details(request):
    if request.user.is_doctor:
        patient = Booking.objects.filter(doctor=request.user.doctor)
        return render(request, 'doctor/doctor_patient_details.html', {'patient': patient})
    else:
        return HttpResponse('Invalid role action')


@login_required
def doctor_single_patient(request, id):
    if request.user.is_doctor:
        try:
            patient_detail = Booking.objects.get(
                doctor=request.user.doctor, id=id)
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
            messages.warning(
                request, 'Old Password and New Password cannot be same.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.get(id=request.user.id)
        # user.password = new_password

        if user.check_password(old_password) == False:
            messages.warning(request, 'Old Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if new_password != request.user.password:
            user.password = make_password(new_password)

        user.save()

        messages.success(
            request, 'Your password has been changed. Please Login Again.')

        auth.logout(request)
        return redirect('login')


# for admin ---------------------------------------------------------------------------------------

@login_required
def admin_dashboard(request):
    if request.user.is_admin:
        all_appointment_details = Booking.objects.filter(
            status=True).order_by('created_on')[:4]
        all_doctor = Doctor.objects.all()
        all_patients = PetOwner.objects.all()

        total_app = all_appointment_details.count()
        total_doc = all_doctor.count()
        total_patients = all_patients.count()
        return render(request, 'admin/admin_dashboard.html', {'appointment_details': all_appointment_details, 'total_app': total_app, 'total_patients': total_patients, 'total_doc': total_doc})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_appointment_details(request):
    if request.user.is_admin:
        appointments_all = Booking.objects.all().order_by('created_on')
        return render(request, 'admin/admin_appointment_history.html', {'appointments_all': appointments_all})
    else:
        return HttpResponse('Invalid Role action')

# service ----- crud operation

@login_required
def admin_service_records(request):
    if request.user.is_admin:
        services = Service.objects.all()
        return render(request, 'admin/admin_service_record.html', {'services': services})
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_add_service(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_add_service.html')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_register_service(request):
    if request.user.is_admin:
        if request.method == 'POST':
            title = request.POST['ser_title']
            price = request.POST['ser_price']
            details = request.POST['ser_details']

            service = Service(title=title, price=price, details=details)
            service.save()

            messages.success(request, 'New Service added.')
            return redirect('admin_service_records')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_edit_service(request, id):
    if request.user.is_admin:
        service = Service.objects.get(id=id)
        return render(request, 'admin/admin_add_service.html', {'service':service})
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_update_service(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            service = Service.objects.get(id=id)
            title = request.POST['ser_title']
            price = request.POST['ser_price']
            details = request.POST['ser_details']

            service.title = title
            service.price = price
            service.details = details

            service.save()

            messages.success(request, 'Service updated successfully.')
            return redirect('admin_service_records')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_delete_service(request, id):
    if request.user.is_admin:
        service = Service.objects.get(id=id)
        service.delete()

        messages.success(request, 'Service deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


# patient ---- operation

@login_required
def admin_patient_record(request):
    if request.user.is_admin:
        patient_record = Booking.objects.filter(status=True)
        return render(request, 'admin/admin_patient_record.html', {'patient': patient_record})
    else:
        return HttpResponse('Invalid Role action')

# petowner ----- crud operation

@login_required
def admin_petowner_record(request):
    if request.user.is_admin:
        petowner_record = PetOwner.objects.all()
        return render(request, 'admin/admin_petowner_record.html', {'petowner': petowner_record})
    else:
        return HttpResponse('Invalid Role action')
    
@login_required
def admin_add_petowner(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_add_petowner.html')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_register_petowner(request):
    if request.user.is_admin:
        if request.method == 'POST':
            first_name = request.POST['pet_first_name']
            last_name = request.POST['pet_last_name']
            username = request.POST['pet_email']
            mobile = request.POST['pet_phone']
            gender = request.POST.get('pet_gender')
            password = request.POST['pet_password']
            confirm_password = request.POST['pet_confirm_password']
            address = request.POST['pet_address']

            is_patient = True

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if PetOwner.objects.filter(mobile=mobile):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=username,
                                            is_patient=is_patient)
            user.save()

            petowner = PetOwner(user=user, mobile=mobile,
                            gender=gender, address=address)
            petowner.save()

            messages.success(request, 'New Pet Owner added with success.')
            return redirect('admin_petowner_records')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_edit_petowner(request, id):
    if request.user.is_admin:
        petowner = PetOwner.objects.get(id=id)
        return render(request, 'admin/admin_add_petowner.html', {'petowner': petowner})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_update_petowner(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            petowner = PetOwner.objects.get(id=id)

            first_name = request.POST['pet_first_name']
            last_name = request.POST['pet_last_name']
            username = request.POST['pet_email']
            mobile = request.POST['pet_phone']
            gender = request.POST.get('pet_gender')
            password = request.POST['pet_password']
            confirm_password = request.POST['pet_confirm_password']
            address = request.POST['pet_address']

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=petowner.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if PetOwner.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = petowner.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.save()

            petowner.mobile = mobile
            petowner.gender = gender
            petowner.address = address
            petowner.save()

            messages.success(request, 'Pet Owner updated successfully.')
            return redirect('admin_petowner_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_delete_petowner(request, id):
    if request.user.is_admin:
        petowner = PetOwner.objects.get(id=id)
        user = petowner.user
        user.delete()
        messages.success(request, 'Pet Owner deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')

# doctor ---- crud operation

@login_required
def admin_doctor_record(request):
    if request.user.is_admin:
        doctor_record = Doctor.objects.all()
        return render(request, 'admin/admin_doctor_record.html', {'doctors': doctor_record})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_add_doctor(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_add_doctor.html')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_register_doctor(request):
    if request.user.is_admin:
        if request.method == 'POST':
            first_name = request.POST['doc_first_name']
            last_name = request.POST['doc_last_name']
            username = request.POST['doc_email']
            mobile = request.POST['doc_phone']
            gender = request.POST.get('doc_gender')
            password = request.POST['doc_password']
            confirm_password = request.POST['doc_confirm_password']
            address = request.POST['doc_address']
            qualification = request.POST['doc_qualification']
            service_type = request.POST['doc_service_type']
            nmc_number = request.POST['doc_nmc_number']

            is_doctor = True

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Doctor.objects.filter(mobile=mobile):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=username,
                                            is_doctor=is_doctor)
            user.save()

            doctor = Doctor(user=user, mobile=mobile,
                            gender=gender, address=address, qualification=qualification, service_type=service_type, nmc_number=nmc_number)
            doctor.save()

            messages.success(request, 'New Doctor added with success.')
            return redirect('admin_doctor_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_edit_doctor(request, id):
    if request.user.is_admin:
        doctor = Doctor.objects.get(id=id)
        return render(request, 'admin/admin_add_doctor.html', {'doctor': doctor})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_update_doctor(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            doctor = Doctor.objects.get(id=id)

            first_name = request.POST['doc_first_name']
            last_name = request.POST['doc_last_name']
            username = request.POST['doc_email']
            mobile = request.POST['doc_phone']
            gender = request.POST.get('doc_gender')
            password = request.POST['doc_password']
            confirm_password = request.POST['doc_confirm_password']
            address = request.POST['doc_address']
            qualification = request.POST['doc_qualification']
            service_type = request.POST['doc_service_type']
            nmc_number = request.POST['doc_nmc_number']

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=doctor.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Doctor.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = doctor.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.save()

            doctor.mobile = mobile
            doctor.gender = gender
            doctor.address = address
            doctor.qualification = qualification
            doctor.service_type = service_type
            doctor.nmc_number = nmc_number
            doctor.save()

            messages.success(request, 'Doctor updated successfully.')
            return redirect('admin_doctor_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_delete_doctor(request, id):
    if request.user.is_admin:
        doctor = Doctor.objects.get(id=id)
        user = doctor.user
        user.delete()
        messages.success(request, 'Doctor deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


# operator -----crud operation

@login_required
def admin_operator_record(request):
    if request.user.is_admin:
        operator_record = Operator.objects.all()
        return render(request, 'admin/admin_operator_record.html', {'operator': operator_record})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_add_operator(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_add_operator.html')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_register_operator(request):
    if request.method == 'POST':
        first_name = request.POST['op_first_name']
        last_name = request.POST['op_last_name']
        username = request.POST['op_email']
        mobile = request.POST['op_phone']
        gender = request.POST.get('op_gender')
        password = request.POST['op_password']
        confirm_password = request.POST['op_confirm_password']
        address = request.POST['op_address']

        is_operator = True

        for value in [first_name, last_name, username, password, confirm_password]:
            if value is None or value == '':
                messages.success(request, 'Provide all information')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if User.objects.filter(username=username):
            messages.warning(request, 'Email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if Operator.objects.filter(mobile=mobile):
            messages.warning(request, 'Phone number already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if password != confirm_password:
            messages.warning(request, 'Password did not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=username,
                                        is_operator=is_operator)
        user.save()

        operator = Operator(user=user, mobile=mobile,
                            gender=gender, address=address)
        operator.save()

        messages.success(request, 'New Operator added with success.')
        return redirect('admin_operator_records')


@login_required
def admin_edit_operator(request, id):
    if request.user.is_admin:
        operator = Operator.objects.get(id=id)
        return render(request, 'admin/admin_add_operator.html', {'operator': operator})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_update_operator(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            operator = Operator.objects.get(id=id)

            first_name = request.POST['op_first_name']
            last_name = request.POST['op_last_name']
            username = request.POST['op_email']
            mobile = request.POST['op_phone']
            gender = request.POST.get('op_gender')
            password = request.POST['op_password']
            confirm_password = request.POST['op_confirm_password']
            address = request.POST['op_address']

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=operator.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Operator.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = operator.user
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.save()

            operator.mobile = mobile
            operator.gender = gender
            operator.address = address
            operator.save()

            messages.success(request, 'Operator updated successfully.')
            return redirect('admin_operator_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_delete_operator(request, id):
    if request.user.is_admin:
        operator = Operator.objects.get(id=id)
        user = operator.user
        user.delete()
        messages.success(request, 'Operator deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')
