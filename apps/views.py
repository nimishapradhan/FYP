from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import connection, IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from .models import UserProfile
from django.urls import reverse
from datetime import date
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages


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
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from doctor_details")
        data = cursor.fetchall()

        doctor_details = []

        for row in data:
            doctor_detail = {
                'id': row[0],
                'name': row[1]
            }
            doctor_details.append(doctor_detail)
        
        print(doctor_details)

        context = {
            'docs': doctor_details
        }


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
            doctor = request.POST['doctor']

            query = "INSERT INTO booking_details (email, phone, address, pet_name, breed, age, color, gender, disease, ongoing_medication, purpose_of_visit, symptom, method, city, tole, house_number, doctor, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (email, phone, address, petname, breed, age, color, gender, nameOfDisease, onGoingMedication, purposeOfVisit, symptonOfDisease, methodOfTreatment, city, tole, houseNumber, date, doctor, time)

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, val)
                    connection.commit()
                return HttpResponseRedirect('/booking')
            except IntegrityError:
                return HttpResponse("Something went wrong")
    else:
        return redirect('login')
    
    return render(request, 'booking.html', context)

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
    current_date = date.today()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE DATE(updatedOn) = %s", [current_date])
        totalPatient = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM doctor_details")
        totalVet = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM booking_details")
        totalAppointment = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM booking_details WHERE DATE(updatedOn) = %s", [current_date])
        todayAppointments = cursor.fetchall()


        appointments = []
        for row in todayAppointments:
            appointment = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'appointment_type': row[11],
                'service_type': row[13],
                'time': row[18],
                'status': 'ongoing',
            }
            appointments.append(appointment)


        sendData = {
            'totalPatients': totalPatient,
            'totalVet': totalVet,
            'totalAppoitment': totalAppointment,
            'todayAppointments': appointments,
        }

    return render(request, 'admin_dashboard.html', sendData)

def admin_app_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        allAppoitments = cursor.fetchall()

        appointments = []
        for row in allAppoitments:
            appointment = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'vet': row[19],
                'appointment_type': row[11],
                'service_type': row[13],
                'time': row[18],
                'date': row[17],
                'status': 'ongoing',
            }
            appointments.append(appointment)
    
        
        sendData = {
            'allAppoitments': appointments,
        }


    return render(request, 'admin_app.html', sendData)

def admin_doctor_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM doctor_details")
        doctors_details = cursor.fetchall()

        doctors = []
        for row in doctors_details:
            docs = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'gender': row[3],
                'phone': row[6],
                'qualification': row[7],
                'service_type': row[8],
                'nmc_number': row[9],
                'address': row[10],
            }
            doctors.append(docs)
    
        
        sendData = {
            'doctors': doctors,
        }


    return render(request, 'admin_doctor.html', sendData)

def admin_patient_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        patients_data = cursor.fetchall()

        patients = []
        for row in patients_data:
            data = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'service_type': row[13],
                'date': row[17]
            }
            patients.append(data)

        sendData = {
            'patients': patients,
        }


    return render(request, 'admin_patient.html', sendData)

def admin_payment_view(request):
    return render(request, 'admin_payment.html')





def usernav_view(request):
    return render(request, 'user_nav.html')

def uhistory_view(request):
    return render(request, 'user_history.html')

# def userdashboard_view(request):
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * from doctor_details")
#         data = cursor.fetchall()

#         user = request.user

#         # cursor.execute("SELECT * FROM booking_details where email = '%s'", [user.email])
#         # Appdata = cursor.fetchall()
#         cursor.execute("SELECT * FROM booking_details")
#         Appdata = cursor.fetchall()

#         doctor_details = []
#         app_details = []

#         for row in data:
#             doctor_detail = {
#                 'id': row[0],
#                 'name': row[1],
#                 'date': row[12],
#                 'time': row[13],
#                 'qualification': row[7],
#                 'status': 'available'
#             }
#             doctor_details.append(doctor_detail)
        
#         for row in Appdata:
#             app_detail = {
#                 'id': row[0],
#                 'date': row[17],
#                 'time': row[18],
#                 'vet': row[19],
#                 'appoitment_type': row[11],
#                 'service_type': row[13]
#             }
#             app_details.append(app_detail)

#     getData = {
#         'doctors': doctor_details,
#         'appoitments': app_details
#     }
#     return render(request, 'user_dashboard.html', getData)


from datetime import date

def userdashboard_view(request):
    with connection.cursor() as cursor:
        # Fetching doctor details
        cursor.execute("SELECT * FROM doctor_details")
        doctor_data = cursor.fetchall()

        user = request.user

        # Fetching appointment details for today's date
        today = date.today()
        print("Date", today)
        cursor.execute("SELECT * FROM booking_details WHERE date = %s", [today])
        app_data = cursor.fetchall()
        
        doctor_details = []
        app_details = []

        # Processing doctor details
        for row in doctor_data:
            doctor_detail = {
                'id': row[0],
                'name': row[1],
                'date': row[12],
                'time': row[13],
                'qualification': row[7],
                'status': 'available'
            }
            doctor_details.append(doctor_detail)

        # Processing appointment details
        for row in app_data:
            app_detail = {
                'id': row[0],
                'date': row[17],
                'time': row[18],
                'vet': row[19],
                'appointment_type': row[11],
                'service_type': row[13]
            }
            app_details.append(app_detail)
        print("Date app", app_details)    

    getData = {
        'doctors': doctor_details,
        'appointments': app_details
    }
    return render(request, 'user_dashboard.html', getData)


def userapp_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        Appdata = cursor.fetchall()

        app_details = []

        for row in Appdata:
            app_detail = {
                'id': row[0],
                'date': row[17],
                'time': row[18],
                'vet': row[19],
                'appoitment_type': row[11],
                'service_type': row[13]
            }
            app_details.append(app_detail)
    
    sendData = {
        'appoitments': app_details
    }
    return render(request, 'user_app.html', sendData)

def userpayment_view(request):
    return render(request, 'user_payment.html')

def userprofile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Error updating your profile. Please check the form.')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'user_profile.html', {'form': form, 'user': user})



def doctordashmain_view(request):
    current_date = date.today()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE DATE(updatedOn) = %s", [current_date])
        totalPatient = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE method = 'home'")
        homePatient = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE method = 'clinic'")
        clinicPatient = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM booking_details WHERE DATE(updatedOn) = %s", [current_date])
        todayAppointments = cursor.fetchall()


        appointments = []
        for row in todayAppointments:
            appointment = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'appointment_type': row[11],
                'service_type': row[13],
                'time': row[18],
                'status': 'ongoing',
            }
            appointments.append(appointment)


        sendData = {
            'totalPatients': totalPatient,
            'home': homePatient,
            'clinic': clinicPatient,
            'todayAppointments': appointments
        }

    return render(request, 'doctordash_main.html', sendData)

def doctorpatient_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        patients_data = cursor.fetchall()

        patients = []
        for row in patients_data:
            data = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'service_type': row[13],
                'date': row[17]
            }
            patients.append(data)

        sendData = {
            'patients': patients,
        }


    return render(request, 'doctor_patient.html', sendData)

# def doctorprofile_view(request):
#     if request.method == 'POST':
#             current_password = request.POST['vet-pw']
#             new_password = request.POST['new-vet-pw']
#             confirm_new_password = request.POST['confirm-new-vet-pw']
    

#     return render(request, 'doctor_profile.html')

def doctorprofile_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('vet-pw', '')
        new_password = request.POST.get('new-vet-pw', '')
        confirm_new_password = request.POST.get('confirm-new-vet-pw', '')

        user = request.user
        print(user.id)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT password
                FROM doctor_details
                WHERE id = %s
            """, [user.id])
            result = cursor.fetchone()

            if not result or not current_password == result[0]:
                return render(request, 'doctor_profile.html', {'error': 'Incorrect current password'})

        if new_password != confirm_new_password:
            return render(request, 'doctor_profile.html', {'error': 'New password and confirm password do not match'})

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE doctor_details
                SET password = %s
                WHERE id = %s
            """, [new_password, user.id])

        return redirect('doctor_profile')
    return render(request, 'doctor_profile.html')

def doctorapp_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        allAppoitments = cursor.fetchall()

        appointments = []
        for row in allAppoitments:
            appointment = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'email': row[1],
                'vet': row[19],
                'appointment_type': row[11],
                'service_type': row[13],
                'time': row[18],
                'date': row[17],
            }
            appointments.append(appointment)
    
        
        sendData = {
            'allAppoitments': appointments,
        }


    return render(request, 'doctorapp.html', sendData)

def doctornav_view(request):
    return render(request, 'doctornav.html')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def doc_register_view(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['doc-first-name']
            last_name = request.POST['doc-last-name']
            gender = request.POST.get('doc-gender')
            phone = request.POST['doc-phone']
            qualification = request.POST['doc-qualification']
            service_type = request.POST['doc-service-type']
            nmc_number = request.POST['doc-nmc-number']
            address = request.POST['doc-address']
            email = request.POST['doc-email']
            password = request.POST['doc-password']

            query = "INSERT INTO doctor_details (first_name, last_name, gender, phone, qualification, service_type, nmc_number, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (first_name, last_name, gender, phone, qualification, service_type, nmc_number, address, email, password)

            with connection.cursor() as cursor:
                cursor.execute(query, val)
                connection.commit()

            return redirect('admin_doctor')

        except MultiValueDictKeyError as e:
            return render(request, 'doc_register.html', {'error_message': f'Missing key: {e}'})
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

