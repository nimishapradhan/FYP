import os                                                                     # Importing the 'os' module for interacting with the operating system.
import json                                                                   # Importing the 'json' module for working with JSON data.
import requests                                                               # Importing the 'requests' module for making HTTP requests.
from django.shortcuts import render, redirect                    
from accounts.models import *                                                 # Importing models from the 'accounts' app
from django.contrib.auth.hashers import make_password                         # Importing a function for hashing passwords from Django
from django.contrib import messages, auth                                     
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from service.models import Booking, Service, Time, Payment
from information.models import Contact, Feedback
from django.utils.crypto import get_random_string
from django.core.mail import send_mail                                         # Importing a function for sending emails from Django
from tailtales import settings
from tailtales.settings import MEDIA_URL                                       # Import MEDIA_URL from 'tailtales.settings'
from reportlab.pdfgen import canvas                                            # Importing modules for generating PDFs from ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse, reverse_lazy                                         # Importing functions for reversing URLs from Django
from django.contrib.auth import authenticate, login
# Create your views here.


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

# Define a function named 'do_register' which handles registration requests
def do_register(request):
    if request.method == 'POST':                                    # When a form is submitted with the 'POST' method, the data from the form fields is sent to the server in the request body, allowing the server to process and handle the data accordingly.
        first_name = request.POST['reg-first-name']
        last_name = request.POST['reg-last-name']
        username = request.POST['reg-email']
        mobile = request.POST['reg-phone']
        gender = request.POST.get('reg-gender')
        password = request.POST['reg-password']
        confirm_password = request.POST['reg-confirm-password']
        address = request.POST['reg-address']

         # Set a flag indicating whether the user is a patient
        is_patient = True
        
        # Check if any required field is empty
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
        

        # Validate the password against Django's built-in password validation rules
        try:
            validate_password(password)
        except:
            messages.warning(request, 'Password must match all the requirements.')
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
            messages.success(request, 'Login Successful')
            return redirect('operator_dashboard')
        else:
            messages.warning(request, 'Username or Password is invalid.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    messages.warning(request, 'Invalid credentials')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out')
    return HttpResponseRedirect('feedback')

def feedback(request):
    return render(request, 'feedback.html')

def save_feedback(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        details = request.POST['details']

        feed_back = Feedback(full_name=full_name, email=email, details=details)
        feed_back.save()
        messages.success(request, 'Thank you for your feedback.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# for pet owner / patient

@login_required
def user_dashboard(request):
    if request.user.is_patient:
        today_date = datetime.now().date()

        doctor = Doctor.objects.filter(status=True)
        appointment = Booking.objects.filter(
            user=request.user, status=True, date__gte=today_date).order_by('date')[:4]
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

# -----------------------------------------------------------------------
    
# function ma Django ko Canvas use garera table bhaneko parameter pa chai payment ko lagi ho,  data ma tei pa lai use garera booking table bata id, user ko name, doctor ko name ani property haru taneko ani data ra header data lai jodeko tyo table banaunua, style tyo color haru dina and tableWrapOn ley size and table.drawOn ley tyo position determine garcha ani last ma save gareko ho.

def generate_pdf(response, payments):
    response['Content-Disposition'] = 'attachment; filename="payment_history.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    image_path = os.path.abspath('././static/image/logo.png')
    p.drawImage(ImageReader(image_path), 200, 680, width=200, height=100, preserveAspectRatio=True)

    main_header_text = "------- Tailtales Transaction Details -------"
    p.setFont("Helvetica-Bold", 16)
    p.setFillColorRGB(0, 0.5, 0)
    p.drawString(165, 645, main_header_text)

    header_data = [["Booking ID", "Pet Owner", "Doctor","Service", "Booking Type", "Amount", "Payment Method", "Paid Date"]]
    
    data = [[
        str(pa.booking.id),
        pa.booking.user.get_full_name(),
        pa.booking.doctor.user.get_full_name(),
        pa.booking.service.title,
        pa.booking.booking_type,
        str(pa.booking.service.price),
        pa.payment_method,
        pa.created_on.strftime("%Y-%m-%d %H:%M:%S")
    ] for pa in payments]

    all_data = header_data + data

    total_amount = sum(float(pa.booking.service.price) for pa in payments)
    total_row = ["Total Amount", "", "", "","", f"{total_amount}", "", ""]
    all_data.append(total_row)
    table = Table(all_data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.whitesmoke),
    ])

    table.setStyle(style)

    table.wrapOn(p, 0, 0)
    table.drawOn(p, 0, 450)

    p.save()

@login_required
def user_download_payment_all(request):
    if request.user.is_patient:
        try:
            bookings = Booking.objects.filter(user=request.user)
            pay_ment = Payment.objects.filter(booking__in=bookings)

            response = HttpResponse(content_type='application/pdf')

            generate_pdf(response, pay_ment)

            return response
        except:
            return HttpResponse('No payment history found')
    else:
        return HttpResponse('Invalid role')


@login_required
def user_download_single_payment(request, id):
    if request.user.is_patient:
        try:
            payment_user = Payment.objects.get(id=id, booking__user=request.user)

            response = HttpResponse(content_type='application/pdf')

            generate_single_bill(response, payment_user)

            return response
        except Payment.DoesNotExist:
            return HttpResponse('Payment not found')
    else:
        return HttpResponse('Invalid role')
    
# -------------------------------------------------------

@login_required
def user_payment_list(request):
    if request.user.is_patient:
        booking = Booking.objects.filter(user=request.user)
        payment = Payment.objects.filter(booking__in=booking)
        return render(request, 'user/payment_history.html', {'payment':payment})
    else:
        return HttpResponse('Invalid role')


# @login_required
# def user_generate_bill(request):
#     if request.user.is_patient:
#         return render(request, 'user/generate_bill.html')
#     else:
#         return HttpResponse('Invalid role')


@login_required
def user_profile(request):
    if request.user.is_patient:
        return render(request, 'user/user_profile.html')
    else:
        return HttpResponse('Invalid role')

@login_required
def user_delete_account(request, id):
    remove_user = User.objects.get(id=id)
    remove_user.delete()

    auth.logout(request)

    messages.success(request, 'Your account has been deleted.')
    return redirect('login')


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


@login_required
def user_cancel_appointment(request, id):
    if request.user.is_patient:
        app = Booking.objects.get(id=id)
        if app.status:
            app.status = False
            app.booking_status = 'Cancelled'
            app.save()
            messages.success(request, 'Appointment Cancelled.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Appointment is already Cancelled.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


@login_required
def user_appointment_detail(request, id):
    if request.user.is_patient:
        try:
            appointment_detail = Booking.objects.get(
                user=request.user, id=id)
        except Booking.DoesNotExist:
            return HttpResponse("You do not have permission to access it.")

        return render(request, 'user/user_single_appointment.html', {'app': appointment_detail})
    else:
        return HttpResponse('Invalid action role')

# for doctor ----


@login_required
def doctor_dashboard(request):
    if request.user.is_doctor:
        today_date = datetime.now().date()

        home_appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True, booking_type='home')
        clinic_appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True, booking_type='clinic')

        appointments = Booking.objects.filter(
            doctor=request.user.doctor, status=True, date__gte=today_date).order_by('date')[:4]

        totalPatients = appointments.count()
        home = home_appointments.count()
        clinic = clinic_appointments.count()

        return render(request, 'doctor/doctor_dashboard.html', {'appointments': appointments, 'totalPatients': totalPatients, 'home': home, 'clinic': clinic})
    else:
        return HttpResponse('Invalid role action.')


@login_required
def doctor_all_appointment(request):
    if request.user.is_doctor:
        appointments = Booking.objects.filter(doctor=request.user.doctor, status=True)
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
        patient = Booking.objects.filter(doctor=request.user.doctor, status=True)
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
        today_date = datetime.now().date()

        all_appointment_details = Booking.objects.filter(
            status=True, date__gte=today_date).order_by('date')[:4]
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
        appointments_all = Booking.objects.all().order_by('date')
        return render(request, 'admin/admin_appointment_history.html', {'appointments_all': appointments_all})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_single_appointment(request, id):
    if request.user.is_admin:
        single_appointment = Booking.objects.get(id=id)
        return render(request, 'admin/admin_single_appointment.html', {'appointment': single_appointment})
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_cancel_appointment(request, id):
    if request.user.is_admin:
        app = Booking.objects.get(id=id)
        if app.status:
            app.status = False
            app.booking_status = 'Cancelled'
            app.save()
            messages.success(request, 'Appointment Cancelled.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'Appointment is already Cancelled.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_delete_appointment(request, id):
    if request.user.is_admin:
        appoint = Booking.objects.get(id=id)
        appoint.delete()
        messages.success(request, 'Appointment deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_profile(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_profile.html')
    else:
        return HttpResponse('Invalid action role')


@login_required
def admin_profile_update(request):
    if request.user.is_admin:
        if request.method == 'POST':
            first_name = request.POST['admin-first-name']
            last_name = request.POST['admin-last-name']
            email = request.POST['admin-email']
            username = request.POST['admin-email']

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
    else:
        return HttpResponse('Invalid action role')

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
            image = request.FILES.get('ser_image')

            service = Service(title=title, price=price, details=details, image=image)
            service.save()

            messages.success(request, 'New Service added.')
            return redirect('admin_service_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_edit_service(request, id):
    if request.user.is_admin:
        service = Service.objects.get(id=id)
        return render(request, 'admin/admin_add_service.html', {'service': service, 'MEDIA_URL':MEDIA_URL})
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
            image = request.FILES.get('ser_image', None)

            service.title = title
            service.price = price
            service.details = details

            if image:
                service.image = image

            service.save()

            messages.success(request, 'Service updated successfully.')
            return redirect('admin_service_records')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_service_img_remove(request, id):
    if request.user.is_admin:
        ser = Service.objects.get(id=id)
        ser.image = None
        ser.save()
        messages.success(request, 'Image removed successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
    
# admin - payment records
    
@login_required
def admin_payment_history(request):
    if request.user.is_admin:
        payment_record = Payment.objects.all()
        return render(request, 'admin/admin_payment_history.html', {'payment': payment_record})
    else:
        return HttpResponse('Invalid Role action')
    
@login_required
def admin_download_payment_history(request):
    if request.user.is_admin:
        try:
            payment_rec = Payment.objects.all()
            response = HttpResponse(content_type='application/pdf')

            generate_pdf(response, payment_rec)

            return response
        except:
            return HttpResponse('No payment history found')
    else:
        return HttpResponse('Invalid role action')
    


# def generate_single_bill(response, pa):
#     response['Content-Disposition'] = 'attachment; filename="single_payment_detail.pdf"'
#     p = canvas.Canvas(response)

#     image_path = os.path.abspath('././static/image/logo.png')
#     p.drawImage(ImageReader(image_path), 210, 700, width=200, height=100, preserveAspectRatio=True)

#     # Title
#     p.setFont("Helvetica-Bold", 16)
#     p.drawString(240, 670, "Payment Details")

#     # Create data for the table
#     data = [
#         ("Booking ID", pa.booking.id),
#         ("Pet Owner Name", pa.booking.user.get_full_name()),
#         ("Doctor", pa.booking.doctor.user.get_full_name()),
#         ("Service", pa.booking.service.title),
#         ("Booking Type", pa.booking.booking_type),
#         ("Amount", f"NPR. {pa.booking.service.price}"),
#         ("Payment Method", pa.payment_method),
#         ("Paid Date", pa.created_on.strftime('%Y-%m-%d')),
#         ("Booking Date", pa.booking.date),
#         ("Booking Time", pa.booking.time),
#     ]

#     if pa.booking.location:
#         data.append(("Location", pa.booking.location))

#     col_widths = [150, 200]  # Adjust the width of columns as needed
#     table = Table(data, colWidths=col_widths)
    
#     # Create the table
#     table = Table(data)

#     # Style the table
#     style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.green),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ])

#     table.setStyle(style)

#     # Draw the table on the canvas
#     table.wrapOn(p, 1000, 1000)  # Adjust the size as needed
#     table.drawOn(p, 200, 400)  # Adjust the position as needed

#     p.save()
    


# function ma Django ko Canvas use garera table bhaneko parameter pa chai payment ko lagi ho,  data ma tei pa lai use garera booking table bata id, user ko name, doctor ko name ani property haru taneko ani data ra header data lai jodeko tyo table banaunua, style tyo color haru dina and tableWrapOn ley size and table.drawOn ley tyo position determine garcha ani last ma save gareko.
    
def generate_single_bill(response, pa):
    response['Content-Disposition'] = 'attachment; filename="single_payment_detail.pdf"'
    p = canvas.Canvas(response)

    image_path = os.path.abspath('././static/image/logo.png')
    p.drawImage(ImageReader(image_path), 210, 700, width=200, height=100, preserveAspectRatio=True)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(240, 670, "Payment Details")

    header_data = ["Booking ID", "Pet Owner", "Doctor", "Service", "Booking Type", "Amount", "Payment Method", "Paid Date"]

    data = [
        [str(pa.booking.id),
        pa.booking.user.get_full_name(),
        pa.booking.doctor.user.get_full_name(),
        pa.booking.service.title,
        pa.booking.booking_type,
        f"NPR. {pa.booking.service.price}",
        pa.payment_method,
        pa.created_on.strftime("%Y-%m-%d")]
    ]
    
    all_data = [header_data] + data
    table = Table(all_data)
    
    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    table.wrapOn(p, 0, 0)
    table.drawOn(p, 20, 550)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(220, 450, "Thank you! TailTales")

    p.save()




@login_required
def admin_payment_single_download(request, id):
    if request.user.is_admin:
        single_pay = Payment.objects.get(id=id)

        response = HttpResponse(content_type='application/pdf')

        generate_single_bill(response, single_pay)

        return response

    else:
        return HttpResponse('Invalid role action')

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
            
            try:
                validate_password(password)
            except:
                messages.warning(request, 'Password must match all the requirements.')
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
            address = request.POST['pet_address']

            for value in [first_name, last_name, username]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=petowner.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if PetOwner.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
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


@login_required
def admin_petowner_change_password(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            petowner = PetOwner.objects.get(id=id)

            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']

            if new_password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = petowner.user
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password has been changed.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid role action')

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
            image = request.FILES.get('doc_image')

            is_doctor = True

            for value in [first_name, last_name, username, password, confirm_password]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username, email=username):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Doctor.objects.filter(mobile=mobile):
                messages.warning(request, 'Phone number already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            try:
                validate_password(password)
            except:
                messages.warning(request, 'Password must match all the requirements.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=username,
                                            is_doctor=is_doctor)
            user.save()

            doctor = Doctor(user=user, mobile=mobile,
                            gender=gender, address=address, qualification=qualification, service_type=service_type, nmc_number=nmc_number, image=image)
            doctor.save()

            messages.success(request, 'New Doctor added with success.')
            return redirect('admin_doctor_records')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_edit_doctor(request, id):
    if request.user.is_admin:
        doctor = Doctor.objects.get(id=id)
        return render(request, 'admin/admin_add_doctor.html', {'doctor': doctor,'MEDIA_URL':MEDIA_URL})
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
            address = request.POST['doc_address']
            qualification = request.POST['doc_qualification']
            service_type = request.POST['doc_service_type']
            nmc_number = request.POST['doc_nmc_number']
            image = request.FILES.get('doc_image', None)

            status = request.POST.get('doc_status')

            for value in [first_name, last_name, username]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=doctor.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Doctor.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
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

            if image:
                doctor.image=image

            # Sets the doctor's status based on the value in the POST request; 0 for inactive, 1 for active else returns an HttpResponse with 'Invalid' message if the status is neither "0" nor "1".
            if status == "0":
                doctor.status = False
            elif status == "1":
                doctor.status = True
            else:
                return HttpResponse('Invalid')

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

@login_required
def admin_doctor_img_remove(request, id):
    if request.user.is_admin:
        doc_image = Doctor.objects.get(id=id)
        doc_image.image = None
        doc_image.save()
        messages.success(request, 'Image removed successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_doctor_change_password(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            doctor = Doctor.objects.get(id=id)

            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']

            if new_password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = doctor.user
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password has been changed.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid role action')


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
        
        try:
            validate_password(password)
        except:
            messages.warning(request, 'Password must match all the requirements.')
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
            address = request.POST['op_address']

            for value in [first_name, last_name, username]:
                if value is None or value == '':
                    messages.success(request, 'Provide all information')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if User.objects.filter(username=username).exclude(id=operator.user.id):
                messages.warning(request, 'Email already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if Operator.objects.filter(mobile=mobile).exclude(id=id):
                messages.warning(request, 'Phone number already exists')
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


@login_required
def admin_operator_change_password(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            operator = Operator.objects.get(id=id)

            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']

            if new_password != confirm_password:
                messages.warning(request, 'Password did not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = operator.user
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password has been changed.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid role action')


# operator dashboard --------------------------------------

@login_required
def operator_dashboard(request):
    if request.user.is_operator:
        today_date = datetime.now().date()
        doctor_op = Doctor.objects.filter(status=True)[:4]                              # Retrieves up to 4 active doctors
        app_op = Booking.objects.filter(                                                # Retrieves up to 4 upcoming appointments
            status=True, date__gte=today_date).order_by('date')[:4]                        
        return render(request, 'operator/operator_dashboard.html', {'doctors': doctor_op, 'appointment': app_op})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_appointment_all(request):
    if request.user.is_operator:
        app_op_all = Booking.objects.all()
        return render(request, 'operator/operator_appointment_all.html', {'appointment': app_op_all})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_doctor(request):
    if request.user.is_operator:
        doctor_oper = Doctor.objects.all()
        return render(request, 'operator/operator_doctor.html', {'doctors': doctor_oper})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_doctor_edit(request, id):
    if request.user.is_operator:
        doctor = Doctor.objects.get(id=id)
        return render(request, 'operator/operator_doctor_edit.html', {'doctor': doctor})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_doctor_change_status(request, id):
    if request.user.is_operator:
        if request.method == 'POST':
            doctor = Doctor.objects.get(id=id)

            status = request.POST.get('doc_status')

            user = doctor.user
            user.save()

            if status == "0":
                doctor.status = False
            elif status == "1":
                doctor.status = True
            else:
                return HttpResponse('Invalid')

            doctor.save()
            messages.success(request, 'Doctor status changed.')
            return redirect('operator_doctor')
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_petowner(request):
    if request.user.is_operator:
        patient_op = Booking.objects.all()
        return render(request, 'operator/operator_petowner.html', {'patients': patient_op})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_petowner_details(request, id):
    if request.user.is_operator:
        single_pet_details = Booking.objects.get(id=id)
        return render(request, 'operator/operator_petowner_details.html', {'appointment': single_pet_details})
    else:
        return HttpResponse('Invalid action role')


@login_required
def operator_profile(request):
    if request.user.is_operator:
        return render(request, 'operator/operator_profile.html')
    else:
        return HttpResponse('Invalid action role')


@login_required
def admin_timeslots(request):
    if request.user.is_admin:
        time_slots = Time.objects.all()
        return render(request, 'admin/admin_timeslots.html', {'time_slots': time_slots})
    else:
        return HttpResponse('Invalid action role')


@login_required
def admin_add_timeslots(request):
    if request.user.is_admin:
        return render(request, 'admin/admin_add_timeslots.html')
    else:
        return HttpResponse('Invalid action role')


@login_required
def admin_register_timeslots(request):
    if request.user.is_admin:
        if request.method == 'POST':
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']

            time = Time(start_time=start_time, end_time=end_time)
            time.save()

            messages.success(request, 'New time added.')
            return redirect('admin_timeslots')

    else:
        return HttpResponse('Invalid action role')


@login_required
def admin_edit_timeslots(request, id):
    if request.user.is_admin:
        time = Time.objects.get(id=id)
        return render(request, 'admin/admin_add_timeslots.html', {'time': time})
    else:
        return HttpResponse('Invalid action role.')


@login_required
def admin_update_timeslots(request, id):
    if request.user.is_admin:
        if request.method == 'POST':
            time = Time.objects.get(id=id)
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']

            time.start_time = start_time
            time.end_time = end_time
            time.save()

            messages.success(request, 'Time updated successfully.')
            return redirect('admin_timeslots')
    else:
        return HttpResponse('Invalid Role action')


@login_required
def admin_delete_timeslots(request, id):
    if request.user.is_admin:
        time = Time.objects.get(id=id)
        time.delete()

        messages.success(request, 'Time deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_contact(request):
    if request.user.is_admin:
        contacts = Contact.objects.all()
        return render(request, 'admin/admin_contact.html', {'contacts':contacts})
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_contact_delete(request, id):
    if request.user.is_admin:
        contact = Contact.objects.get(id=id)
        contact.delete()
        messages.success(request, 'Contact deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')
    
@login_required
def admin_feedback(request):
    if request.user.is_admin:
        feedbacks = Feedback.objects.all()
        return render(request, 'admin/admin_feedback.html', {'feedback':feedbacks})
    else:
        return HttpResponse('Invalid Role action')

@login_required
def admin_feedback_delete(request, id):
    if request.user.is_admin:
        feedback = Feedback.objects.get(id=id)
        feedback.delete()
        messages.success(request, 'Feedback deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Invalid Role action')

@login_required
def khalti_request(request, id):
    if request.user.is_patient:
        booking = Booking.objects.get(pk=id)
        price = booking.service.price * 100

        return render(request, 'user/khalti_payment_request.html', {'booking': booking, 'price': price})
    else:
        return HttpResponse('Invalid Role action')

@login_required
def initkhalti(request):
    if request.user.is_patient:

        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        return_url = request.POST.get('return_url')
        website_url = request.POST.get('return_url')
        amount = request.POST.get('amount')
        purchase_order_id = request.POST.get('purchase_order_id')

        print("url", url)
        print("return_url", return_url)
        print("web_url", website_url)
        print("amount", amount)
        print("purchase_order_id", purchase_order_id)
        user = request.user
        payload = json.dumps({
            "return_url": return_url,
            "website_url": website_url,
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": user.first_name,
                "email": user.email,
            }
        })
        headers = {
            'Authorization': 'key cf584127ee45498ab259d4b328b2cf69',
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        new_res = json.loads(response.text)
        print(new_res)

        return redirect(new_res['payment_url'])
        # return redirect('user_dashboard')
    else:
        return HttpResponse('Invalid Role action')

@login_required
def verifyKhalti(request):
    if request.user.is_patient:
        pidx = request.GET.get('pidx')
        txnId = request.GET.get('txnId')
        amount = request.GET.get('amount')
        purchase_order_id = request.GET.get('purchase_order_id')

        if pidx and txnId and amount:
            try:

                booking = Booking.objects.get(purchase_id=purchase_order_id)
                booking.booking_status = 'Confirmed'  
                booking.status = True  
                booking.save()

                payment = Payment.objects.create(payment_id=pidx, booking=booking, payment_method='Khalti', payment_completed=True)
                payment.save()

                post_bill_response = post_bill_view(booking)

                send_confirmation_emails(booking)

                if 'result' in post_bill_response:
                    messages.success(request, f"{post_bill_response['message']}. Response Data: {post_bill_response['data']}")
                else:
                    messages.error(request, f"Error code {post_bill_response['error']}: {post_bill_response['message']}. Response Data: {post_bill_response['data']}")

                messages.success(request, 'Payment Verified. Booking Confirmed!')
                return HttpResponseRedirect('user_appointment_list')
            except Booking.DoesNotExist:
                messages.error(request, 'Invalid Booking ID.')
        else:
            messages.error(request, 'Invalid parameters in the callback URL.')

        return HttpResponse(status=400)
    else:
        return HttpResponse('Invalid Role action.')
         

# def send_confirmation_emails(booking):
#     send_email_to_user(booking)
#     send_email_to_doctor(booking)
#     send_email_to_admin(booking)
#     send_email_to_operator(booking)




#  # Defines a function named "send_email_to_user" that takes a single argument "booking".
# def send_email_to_user(booking):
#     subject = 'Appointment Confirmed'                                                  # Assigns a string 'Appointment Confirmed' to the variable "subject".

#     message = f'Dear {booking.user.first_name} {booking.user.last_name},<br><br>'
#     message += f'Your appointment has been confirmed. Your appointment details:<br><br>'
#     message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}<br><br>'
#     message += f'<strong>Service:</strong> {booking.service}<br><br>'
#     message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
#     message += f'<strong>Date:</strong> {booking.date}<br><br>'
#     message += f'<strong>Time:</strong> {booking.time}<br><br>'
#     message += 'Thank You!'

#     from_email = settings.EMAIL_HOST_USER                                          # Retrieves the email host user from the settings.
#     to_email = [booking.user.email]                                                 # Retrieves the user's email address and stores it in a list.

#     send_mail(subject, message, from_email, to_email, html_message=message)               # Calls the send_mail function to send the email with the specified subject, message, sender, recipient, and HTML message.

# def send_email_to_doctor(booking):
#     subject = 'Appointment Confirmed'

#     message = f'Dear {booking.doctor.user.first_name} {booking.doctor.user.last_name},<br><br>'
#     message += f'Appointment has been confirmed:<br><br>'
#     message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
#     message += f'<strong>Service:</strong> {booking.service}<br><br>'
#     message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
#     message += f'<strong>Date:</strong> {booking.date}<br><br>'
#     message += f'<strong>Time:</strong> {booking.time}<br><br>'
#     message += 'Thank You!'

#     from_email = settings.EMAIL_HOST_USER
#     to_email = [booking.doctor.user.email]

#     send_mail(subject, message, from_email, to_email, html_message=message)

# def send_email_to_admin(booking):

#     admin_users = User.objects.filter(is_admin=True)

#     subject = 'Appointment Confirmed'

#     message = f'Appointment has been confirmed:<br><br>'
#     message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
#     message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}  <br><br>'
#     message += f'<strong>Service:</strong> {booking.service}<br><br>'
#     message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
#     message += f'<strong>Date:</strong> {booking.date}<br><br>'
#     message += f'<strong>Time:</strong> {booking.time}<br><br>'
#     message += 'Thank You!'

#     from_email = settings.EMAIL_HOST_USER
#     to_email = [admin_user.email for admin_user in admin_users]

#     send_mail(subject, message, from_email, to_email, html_message=message)

# def send_email_to_operator(booking):
#     operator_users = User.objects.filter(is_operator=True)

#     subject = 'Appointment Confirmed'

#     message = f'Appointment has been confirmed:<br><br>'
#     message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
#     message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}  <br><br>'
#     message += f'<strong>Service:</strong> {booking.service}<br><br>'
#     message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
#     message += f'<strong>Date:</strong> {booking.date}<br><br>'
#     message += f'<strong>Time:</strong> {booking.time}<br><br>'
#     message += 'Thank You!'

#     from_email = settings.EMAIL_HOST_USER
#     to_email = [operator_user.email for operator_user in operator_users]

#     send_mail(subject, message, from_email, to_email, html_message=message)
    


def send_confirmation_emails(booking):
    send_email_to_user(booking)
    send_email_to_doctor(booking)
    send_email_to_admin(booking)
    send_email_to_operator(booking)




 # Defines a function named "send_email_to_user" that takes a single argument "booking".
def send_email_to_user(booking):
    subject = 'Appointment Confirmed'                                                  # Assigns a string 'Appointment Confirmed' to the variable "subject".

    message = f'Dear {booking.user.first_name} {booking.user.last_name},<br><br>'
    message += f'Your appointment has been confirmed. Your appointment details:<br><br>'
    message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}<br><br>'
    message += f'<strong>Service:</strong> {booking.service}<br><br>'
    message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
    message += f'<strong>Date:</strong> {booking.date}<br><br>'
    message += f'<strong>Time:</strong> {booking.time}<br><br>'
    message += 'Thank You!'

    from_email = settings.EMAIL_HOST_USER                                          # Retrieves the email host user from the settings.
    to_email = [booking.user.email]                                                 # Retrieves the user's email address and stores it in a list.

    send_mail(subject, message, from_email, to_email, html_message=message)               # Calls the send_mail function to send the email with the specified subject, message, sender, recipient, and HTML message.

def send_email_to_doctor(booking):
    subject = 'Appointment Confirmed'

    message = f'Dear {booking.doctor.user.first_name} {booking.doctor.user.last_name},<br><br>'
    message += f'Appointment has been confirmed:<br><br>'
    message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
    message += f'<strong>Service:</strong> {booking.service}<br><br>'
    message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
    message += f'<strong>Date:</strong> {booking.date}<br><br>'
    message += f'<strong>Time:</strong> {booking.time}<br><br>'
    message += 'Thank You!'

    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.doctor.user.email]

    send_mail(subject, message, from_email, to_email, html_message=message)

def send_email_to_admin(booking):

    admin_users = User.objects.filter(is_admin=True)

    subject = 'Appointment Confirmed'

    message = f'Appointment has been confirmed:<br><br>'
    message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
    message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}  <br><br>'
    message += f'<strong>Service:</strong> {booking.service}<br><br>'
    message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
    message += f'<strong>Date:</strong> {booking.date}<br><br>'
    message += f'<strong>Time:</strong> {booking.time}<br><br>'
    message += 'Thank You!'

    from_email = settings.EMAIL_HOST_USER
    to_email = [admin_user.email for admin_user in admin_users]

    send_mail(subject, message, from_email, to_email, html_message=message)

def send_email_to_operator(booking):
    operator_users = User.objects.filter(is_operator=True)

    subject = 'Appointment Confirmed'

    message = f'Appointment has been confirmed:<br><br>'
    message += f'<strong>Pet Owner:</strong> {booking.user.first_name} {booking.user.last_name}  <br><br>'
    message += f'<strong>Doctor:</strong> {booking.doctor.user.first_name} {booking.doctor.user.last_name}  <br><br>'
    message += f'<strong>Service:</strong> {booking.service}<br><br>'
    message += f'<strong>Booking Type:</strong> {booking.booking_type}<br><br>'
    message += f'<strong>Date:</strong> {booking.date}<br><br>'
    message += f'<strong>Time:</strong> {booking.time}<br><br>'
    message += 'Thank You!'

    from_email = settings.EMAIL_HOST_USER
    to_email = [operator_user.email for operator_user in operator_users]

    send_mail(subject, message, from_email, to_email, html_message=message)
    
    



    



# forget password

# def forget_password(request):
#     try:
#         if request.method == 'POST':
#             email = request.POST['email']

#             if not User.objects.filter(email=email).first():
#                 messages.warning(request, 'No email found.')
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
#             otp = get_random_string(length=6, allowed_chars='1234567890')

#             request.session['reset_email'] = email 

#             user = User.objects.get(email=email)
#             user.otp = otp
#             user.save()

#             subject = 'Forget Password'
        
#             message = f'Hello {user.first_name} {user.last_name},<br><br>'
#             message += 'You requested a password reset. Please use the following OTP to proceed:<br><br>'
#             message += f'<strong>OTP: {otp}</strong><br><br>'
#             message += 'This OTP is valid for 15 minutes.<br>'
#             message += 'If you did not request a password reset, please ignore this email.<br><br>'
#             message += 'Thank You!'

#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [user.email]

#             send_mail(subject, message, from_email, recipient_list, html_message=message)

#             return render(request, 'forget_password/otp.html')
#     except:
#         messages.warning(request, 'Invalid')
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
#     return render(request,'forget_password/forget_password.html')

from django.template.loader import render_to_string

def forget_password(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']

            if not User.objects.filter(email=email).first():
                messages.warning(request, 'No email found.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            otp = get_random_string(length=6, allowed_chars='1234567890')

            request.session['reset_email'] = email 

            user = User.objects.get(email=email)
            user.otp = otp
            user.save()

            subject = 'Forget Password'

            # Use the render_to_string function to render the email template
            email_template = render_to_string('forget_password/reset_password_email_template.html', {'user': user, 'otp': otp})

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, None, from_email, recipient_list, html_message=email_template)

            return render(request, 'forget_password/otp.html')
    except:
        messages.warning(request, 'Invalid')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'forget_password/forget_password.html')

def verify_otp(request):
    try:
        if request.method == 'POST':
            email = request.session.get('reset_email')
            otp_entered = request.POST.get('otp')

            user = User.objects.filter(email=email).first()

            if user and user.otp == otp_entered:
                user.otp_verified = True
                user.save()

                return render(request, 'forget_password/reset_password.html', {'otp_verified': True, 'email': email})
            else:
                messages.warning(request, 'Invalid OTP. Please try again.')
                return render(request, 'forget_password/otp.html', {'otp_verified': False, 'email': email})

    except Exception as e:
        print(e)
        messages.warning(request, 'Invalid')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return HttpResponse("Unexpected error or invalid request.")

def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if new_password == confirm_password:
            user = User.objects.filter(email=email).first()

            if user:
                user.password = make_password(new_password)
                user.otp = None
                del request.session['reset_email']
                user.save()

                subject = 'Password Changed'
        
                message = f'Hello {user.first_name} {user.last_name},<br><br>'
                message += 'Your password has been changed.<br><br>'
                message += 'Thank You!'

                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user.email]

                send_mail(subject, message, from_email, recipient_list, html_message=message)

                messages.success(request, 'Password changed with success.!!!')
                return redirect('login')
            else:
                error = "User not found."
                return render(request, 'forget_password/reset_password.html', {'error': error, 'email': email})
        else:
            error = "Passwords do not match."
            return render(request, 'forget_password/reset_password.html', {'error': error, 'email': email})
    else:
        return HttpResponseRedirect('login')

# ird api called to post the bill for verification

def post_bill_view(booking):
    api_url = "https://cbapi.ird.gov.np/api/bill"

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "username": booking.user.email,
        "password": booking.user.password,
        "seller_pan": "999999999",
        "buyer_pan": "123456789",
        "buyer_name": booking.user.first_name,
        "fiscal_year": "2073.074",
        # "invoice_number": str(booking.id),
        "invoice_number": get_random_string(length=9, allowed_chars='1234567890'),
        "invoice_date": "2074.07.06",
        "total_sales": 1130,
        "taxable_sales_vat": 1000,
        "vat": 130,
        "excisable_amount": 0,
        "excise": 0,
        "taxable_sales_hst": 0,
        "hst": 0,
        "amount_for_esf": 0,
        "esf": 0,
        "export_sales": 0,
        "tax_exempted_sales": 0,
        "isrealtime": True,
        "datetimeclient": datetime.now().isoformat(),
    }
    print(payload)
    try:
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)

        print(response.json())

        if response.status_code == 200:
            return {"result": response.status_code, "message": "Payment verification successful.","data": response.json()}
        else:
            return {"error": f"Error code {response.status_code}", "message": "Payment verification failed.", "data": response.json()}

    except Exception as e:
        return {"error": str(e), "message": "An error occurred during payment verification."}