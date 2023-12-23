from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import connection, IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.hashers import make_password
from .models import UserProfile
from django.urls import reverse
from datetime import date
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def service_view(request):
    return render(request, 'service.html')

def team_view(request):
    return render(request, 'team.html')

def admin_login(request):
    if request.method == 'POST':
        getEmail = request.POST['admin_login_email']
        getPassword = request.POST['admin_login_password']
        sql_query = "Select * from admin_profile WHERE email = %s and password =%s"

        values = (getEmail, getPassword)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            data= cursor.fetchone()
        
   
        if data :
            print("test1",data)
            return HttpResponseRedirect("/admin_dashboard")
            
        
        else:
            return HttpResponse("Invalid Login")

    return render(request, 'admin_login.html')
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
            val = (email, phone, address, petname, breed, age, color, gender, nameOfDisease, onGoingMedication, purposeOfVisit, symptonOfDisease, methodOfTreatment, city, tole, houseNumber,  doctor, date, time)

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
    if request.method == 'POST':
        email = request.POST['email']
        with connection.cursor() as cursor:
            # Use raw SQL query to get the user based on email
            cursor.execute("SELECT * FROM auth_user WHERE email = %s", [email])
            row = cursor.fetchone()

        if row:
            user_id = row[0]
            username = row[4]
            db_email = row[7]

            # Generate OTP
            otp = get_random_string(length=6, allowed_chars='1234567890')

            # Store OTP in the database
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE auth_user SET otp = %s, otp_created_at = %s WHERE id = %s",
                    [otp, timezone.now(), user_id]
                )

            # Send OTP via Email
            subject = 'Forget Password'
            
            message = f'Hello {username},<br><br>'
            message += 'You requested a password reset. Please use the following OTP to proceed:<br><br>'
            message += f'<strong>OTP: {otp}</strong><br><br>'
            message += 'This OTP is valid for 15 minutes.<br>'
            message += 'If you did not request a password reset, please ignore this email.<br><br>'
            message += 'Thank You!'

            from_email = 'Nimisha'
            recipient_list = [db_email]

            send_mail(subject, message, from_email, recipient_list, html_message=message)

            return render(request, 'password.html', {'otp_sent': True, 'email': db_email})
        else:
            return render(request, 'password.html', {'user_not_found': True, 'error': 'Email not found!'})
    else:
        return render(request, 'password.html', {'otp_sent': False, 'otp_verified': False})

def verify_otp(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            otp_entered = request.POST['otp']

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM auth_user WHERE email = %s AND otp = %s AND otp_created_at >= %s",
                    [email, otp_entered, timezone.now() - timezone.timedelta(minutes=15)]
                )
                row = cursor.fetchone()

            if row:
                user_id = row[0]
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE auth_user SET otp_verified = TRUE WHERE id = %s", [user_id])

                return render(request, 'passwordreset.html', {'otp_verified': True, 'email': email})
            else:
                return render(request, 'passwordreset.html', {'otp_verified': False, 'email': email})
        except MultiValueDictKeyError:
            return render(request, 'passwordreset.html', {'otp_verified': False, 'email_not_found': True})
    else:
        return render(request, 'passwordreset.html', {'otp_verified': False, 'otp_sent': False})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if new_password == confirm_password:
            hashed_password = make_password(new_password)
            with connection.cursor() as cursor:
                cursor.execute("UPDATE auth_user SET password = %s WHERE email = %s", [hashed_password, email])
            return HttpResponseRedirect('/login')
        else:
            error = "Passwords do not match."
            return render(request, 'passwordreset.html', {'otp_verified': True, 'error': error, 'email': email})
    else:
        return HttpResponseRedirect('/login')

def faq_view(request):
    return render(request, 'faq.html')

def feedback_view(request):
    return render(request, 'feedback.html')

def terms_view(request):
    return render(request, 'terms.html')

def payment_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        getData = cursor.fetchall()

        storeData = []
        for row in getData:
            service_name = row[11]
            print(service_name)
            cursor.execute("SELECT * FROM service_details WHERE service_name = %s", [service_name])
            service_data = cursor.fetchone()
            print(service_data)
            data = {
                'date': row[17],
                'pet': row[4],
                'email': row[1],
                'servicetype': row[11],
                'cost': service_data[2],
            }
            storeData.append(data)

        sendData = {
            'payments': storeData,
        }
    return render(request, 'payment.html', sendData)




def adminnav_view(request):
    return render(request, 'admin_nav.html')


def admin_service_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM service_details")
        service_details = cursor.fetchall()

        services = []
        for row in service_details:
            service = {
                'service_id': row[0],
                'service_name': row[1],
                'service_price': row[2],
                'service_description': row[3],
            }
            services.append(service)

        sendData = {
            'service_details': services,
        }

    return render(request, 'admin_service.html', sendData)



def edit_service_admin(request, service_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE service_details SET service_name = %s, service_price = %s, "
                    "service_description = %s WHERE service_id = %s",
                    [
                        request.POST.get('service_name', ''),
                        request.POST.get('service_price', ''),
                        request.POST.get('service_description', ''),
                        service_id,
                    ]
                )
        except Exception as e:
            print(f"Error updating service details: {e}")
            return redirect('error_page')  # Redirect to your error page

        return redirect('admin_service')
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM service_details WHERE service_id = %s", [service_id])
                service_details = cursor.fetchone()

                if not service_details:
                    return redirect('not_found')  # Redirect to a not found page

                service = {
                    'service_id': service_details[0],
                    'service_name': service_details[1],
                    'service_price': service_details[2],
                    'service_description': service_details[3],
                }

        except Exception as e:
            print(f"Error fetching service details: {e}")
            return redirect('error_page')  # Redirect to your error page

        return render(request, 'edit_service_admin.html', {'service': service})


def delete_service_admin(request, service_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM service_details WHERE service_id = %s", [service_id])

    return redirect('admin_service')



def admin_cancelled_appointment(request):
     status = 'Cancelled'
     with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details Where status= %s", [status])
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
                'status': 'Cancelled',
            }
            appointments.append(appointment)
    
        
        sendData = {
            'allAppoitments': appointments,
        }


        return render(request, 'admin_cancelled_appointment.html', sendData)

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
                'email': row[4],
                'qualification': row[7],
                'service_type': row[8],
                'nmc_number': row[9],
                'address': row[10],
                'status': row[14],
            }
            doctors.append(docs)
    
        
        sendData = {
            'doctors': doctors,
        }

    return render(request, 'admin_cancelled_appointment.html')


def delete_doctor_admin(request, doctor_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM doctor_details WHERE id = %s", [doctor_id])

    return HttpResponseRedirect('/admin_doctor')



def edit_doctor_admin(request, doctor_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE doctor_details SET first_name = %s, last_name = %s, gender = %s, "
                    "phone = %s, qualification = %s, service_type = %s, "
                    "nmc_number = %s, address = %s, email = %s, status = %s WHERE id = %s",
                    [
                        request.POST.get('first_name', ''),
                        request.POST.get('last_name', ''),
                        request.POST.get('gender', ''),
                        request.POST.get('phone', ''),
                        request.POST.get('qualification', ''),
                        request.POST.get('service_type', ''),
                        request.POST.get('nmc_number', ''),
                        request.POST.get('address', ''),
                        request.POST.get('email', ''),
                        request.POST.get('status', ''),
                        doctor_id,
                    ]
                )
        except Exception as e:
            # Handle the exception, you may want to log it or redirect to an error page
            print(f"Error updating doctor details: {e}")
            return HttpResponseRedirect('/error_page/')  # Redirect to your error page

        # After updating, redirect to the admin_doctor page
        return redirect('admin_doctor')
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM doctor_details WHERE id = %s", [doctor_id])
                doctor_details = cursor.fetchone()

                if not doctor_details:
                    # Handle the case where doctor with the given ID is not found
                    return HttpResponseRedirect('/not_found/')  # Redirect to a not found page

                doctor = {
                    'id': doctor_details[0],
                    'first_name': doctor_details[1],
                    'last_name': doctor_details[2],
                    'gender': doctor_details[3],
                    'phone': doctor_details[4],
                    'qualification': doctor_details[5],
                    'service_type': doctor_details[6],
                    'nmc_number': doctor_details[7],
                    'address': doctor_details[8],
                    'email': doctor_details[9],
                    'status': doctor_details[10],
                }

        except Exception as e:
            # Handle the exception, you may want to log it or redirect to an error page
            print(f"Error fetching doctor details: {e}")
            return HttpResponseRedirect('/error_page/')  # Redirect to your error page

        return render(request, 'edit_doctor_admin.html', {'doctor': doctor})



def admin_dashboard(request):
    current_date = date.today()
    status = 'Ongoing'

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE date = %s", [current_date] )
        totalPatient = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM doctor_details")
        totalVet = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM booking_details")
        totalAppointment = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM booking_details WHERE date = %s AND status =%s", [current_date, status])
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


def cancel_appointment(request, appointment_id):
    with connection.cursor() as cursor:
        # Write your raw SQL query to update the appointment status
        sql_query = "UPDATE booking_details SET status = 'Cancelled' WHERE id = %s"
        cursor.execute(sql_query, [appointment_id])

    
    return redirect( 'admin_dashboard')  # Redirect to the appointment list page


def admin_app_view(request):
    status = 'Cancelled'
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details WHERE status != %s", [status])
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
                'status': row[21],
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
                'email': row[4],
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
                'pet_breed': row[5],
                'pet_age': row[6],
                'pet_colour': row[7],
                'gender': row[8],
                'email': row[1],
                'tole': row[15],
                'number': row[2],
                'address': row[3],
                'housenumber': row[16],
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
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        patients_data = cursor.fetchall()

        patients = []
        for row in patients_data:
            data = {
                'appointment_id': row[0],
                'pet_name': row[4],
                'pet_breed': row[5],
                'pet_age': row[6],
                'pet_colour': row[7],
                'gender': row[8],
                'email': row[1],
                'tole': row[15],
                'number': row[2],
                'address': row[3],
                'housenumber': row[16],
            }
            patients.append(data)

        sendData = {
            'patients': patients,
        }

    return render(request, 'user_history.html', sendData)

  

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
        # print("Date app", app_details)    

    getData = {
        'doctors': doctor_details,
        'appointments': app_details
    }
    return render(request, 'user_dashboard.html', getData)


def delete_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        print(appointment_id)

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM booking_details WHERE id = %s", [appointment_id])
    
    return HttpResponseRedirect('/user_app')

def delete_appointment_doc(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        print(appointment_id)

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM booking_details WHERE email = %s", [appointment_id])
    
    return HttpResponseRedirect('/doctorapp')

def delete_appointment_admin(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')

        print(appointment_id)

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM booking_details WHERE email = %s", [appointment_id])
    
    return HttpResponseRedirect('/admin_app')


def delete_patient_admin(request):
    if request.method == 'POST':
        patient_email = request.POST.get('patient_email')

        try:
            with connection.cursor() as cursor:
                # Use parameterized query to prevent SQL injection
                cursor.execute("DELETE FROM booking_details WHERE email = %s", [patient_email])

            # Redirect after successful deletion to avoid form resubmission
            return redirect('/admin_patient')

        except Exception as e:
            # Handle the exception (e.g., log it or show an error message)
            print(f"Error deleting patient: {e}")

    # If the request method is not POST or deletion fails, redirect to some error page
    return redirect('/error_page')






def userapp_view(request):
    userid = request.user.email
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details where email = %s", {userid})
        Appdata = cursor.fetchall()

        app_details = []

        for row in Appdata:
            app_detail = {
                'id': row[0],
                'date': row[17],
                'time': row[18],
                'vet': row[19],
                'appointment_type': row[13],
                'service_type': row[11]
            }
            app_details.append(app_detail)
    
    sendData = {
        'appointments': app_details
    }

    # print(app_details)
    return render(request, 'user_app.html', sendData)   

def userpayment_view(request):
    return render(request, 'user_payment.html')




def userprofile_view(request):
    user = request.user
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user.first_name = request.POST.get('user-first-name')
            user.last_name = request.POST.get('user-last-name')
            user.email = request.POST.get('user-email')
            user.save()
            messages.success(request, 'Profile updated successfully')
        
        elif 'change_password' in request.POST:
            # Password change handling
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Validate the current password
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Update the user's session
                    messages.success(request, 'Password changed successfully')

                else:
                    messages.error(request, 'New password and confirmation do not match')
            else:
                messages.error(request, 'Current password is incorrect')
    context = {
        'user': user,
        #'password_form': form,
    }
    return render(request, 'user_profile.html', context)


# def profile(request):
#     user = request.user
    
#     if request.method == 'POST':
#         if 'update_profile' in request.POST:
#             # user.username = request.POST.get('username')
#             user.first_name = request.POST.get('fullname')
#             user.email = request.POST.get('email')
#             user.save()
#             messages.success(request, 'Profile updated successfully')

#         if 'change_password' in request.POST:
#             # Password change handling
#             current_password = request.POST.get('current_password')
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('confirm_password')

#             # Validate the current password
#             if user.check_password(current_password):
#                 if new_password == confirm_password:
#                     user.set_password(new_password)
#                     user.save()
#                     update_session_auth_hash(request, user)  # Update the user's session
#                     messages.success(request, 'Password changed successfully')
                    
#                 else:
#                     messages.error(request, 'New password and confirmation do not match')
#             else:
#                 messages.error(request, 'Current password is incorrect')

#     context = {
#         'user': user
#     }
#     return render(request, 'profile.html', context)



#def userprofile_view(request):
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
    status =  'Cancelled'
    user_id = request.user

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE date = %s", [current_date])
        totalPatient = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE method = 'home'")
        homePatient = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM booking_details WHERE method = 'clinic'")
        clinicPatient = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM booking_details WHERE date = %s and status != %s", [current_date, status])
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
                'status': row[21],
                'age': row[6],
                'breed':row[5],
                'color':row[7],
                'address': row[3],
                'contact':row[2],
                'description': row[11]
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
        allAppointments = cursor.fetchall()

        appointments = []
        for row in allAppointments:
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

def xyz_view(request):
    return render(request, 'xyz.html')

def invoice_view(request):
    return render(request, 'invoice.html')

def oappointment_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM booking_details")
        allAppointments = cursor.fetchall()

        appointments = []
        for row in allAppointments:
            appointment = {
                'pet_name': row[4],
                'email': row[1],
                'vet': row[19],
                'appointment_type': row[11],
                'service_type': row[13],
                'time': row[18],
                'date': row[17],
                'status': row[21]
            }
            appointments.append(appointment)
    
        
        sendData = {
            'allAppoitments': appointments,
        }
    return render(request, 'oappointment.html', sendData)
    



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




def operator_register_view(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['op-first-name']
            last_name = request.POST['op-last-name']
            gender = request.POST.get('op-gender')
            phone = request.POST['op-phone']
            address = request.POST['op-address']
            email = request.POST['op-email']
            password = request.POST['op-password']

            query = "INSERT INTO operator_details (first_name, last_name, gender, phone, address, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (first_name, last_name, gender, phone, address, email, password)

            with connection.cursor() as cursor:
                cursor.execute(query, val)
                connection.commit()

            return redirect('admin_operator')

        except MultiValueDictKeyError as e:
            return render(request, 'operator_register.html', {'error_message': f'Missing key: {e}'})
    return render(request, 'operator_register.html')




def login_view(request):
    if request.method == 'POST':
        getEmail = request.POST['login-email']
        getPassword = request.POST['login-password']
        getUserRole = request.POST['user_role']

        user = None
        if getUserRole == 'patient':
            user = authenticate(request, username=getEmail, password=getPassword)
        elif getUserRole == 'doctor':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM doctor_details WHERE email = %s AND password = %s", (getEmail, getPassword))
                getData = cursor.fetchone()
            
            if getData:
                return HttpResponseRedirect('/doctordash_main')

        elif getUserRole == 'operator':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM operator_details WHERE email = %s AND password = %s", (getEmail, getPassword))
                getData = cursor.fetchone()
            
            if getData:
                return HttpResponseRedirect('/odashboard')
        elif getUserRole == 'admin':
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM admin_profile WHERE email = %s AND password = %s", (getEmail, getPassword))
                getData = cursor.fetchone()
            
            if getData:
                return HttpResponseRedirect('/admin_dashboard')

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
    return render(request, 'login.html')

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard')



def odashboard(request):
    try:
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
            # print("Date app", app_details)    

        getData = {
            'doctors': doctor_details,
            'appointments': app_details
        }

        return render(request, 'odashboard.html', getData)

    except Exception as e:
        # Handle exceptions (print or log the error, or redirect to an error page)
        print(f"An error occurred: {e}")
        # Redirect to an error page or handle the error accordingly
        return render(request, 'error_page.html', {'error_message': str(e)})

    


def odoctor(request):
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
                'email': row[4],
                'qualification': row[7],
                'service_type': row[8],
                'nmc_number': row[9],
                'address': row[10],
            }
            doctors.append(docs)
    
        sendData = {
            'doctors': doctors,
        }

    return render(request, 'odoctor.html', sendData)



def opatient(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booking_details")
            patients_data = cursor.fetchall()

            patients = []
            for row in patients_data:
                data = {
                    'appointment_id': row[0],
                    'pet_name': row[4],
                    'pet_breed': row[5],
                    'pet_age': row[6],
                    'pet_colour': row[7],
                    'gender': row[8],
                    'email': row[1],
                    'tole': row[15],
                    'number': row[2],
                    'address': row[3],
                    'housenumber': row[16],
                }
                patients.append(data)

            sendData = {
                'patients': patients,
            }

        return render(request, 'opatient.html', sendData)

    except Exception as e:
        # Handle exceptions (print or log the error, or redirect to an error page)
        print(f"An error occurred: {e}")
        # Redirect to an error page or handle the error accordingly
        return render(request, 'error_page.html', {'error_message': str(e)})



def oprofile(request):
    return render(request, 'oprofile.html')


def admin_operator(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM operator_details")
        operator_details = cursor.fetchall()

        operators = []
        for row in operator_details:
            operator = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'gender': row[3],
                'phone': row[7],
                'email': row[4],
                'address': row[6],
            }
            operators.append(operator)

        sendData = {
            'operators_data': operators,
        }

    return render(request, 'admin_operator.html', sendData)

def delete_operator(request, operator_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM operator_details WHERE id = %s", [operator_id])
    
    return redirect('admin_operator')



def edit_operator(request, operator_id):
    if request.method == 'POST':
        # Handle form submission and update operator details in the database
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE operator_details SET first_name = %s, last_name = %s, gender = %s, "
                "email = %s, address = %s, phone = %s WHERE id = %s",
                [
                    request.POST['first_name'],
                    request.POST['last_name'],
                    request.POST['gender'],
                    request.POST['email'],
                    request.POST['address'],
                    request.POST['phone'],
                    operator_id,
                ]
            )

        # After updating, redirect to the admin_operator page
        return redirect('admin_operator')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM operator_details WHERE id = %s", [operator_id])
            operator_details = cursor.fetchone()

            if not operator_details:
                # Handle the case where operator with the given ID is not found
                # For simplicity, redirect to an error page. You can customize this behavior.
                return redirect('error_page')  # Replace 'error_page' with your actual error page

            operator = {
                'id': operator_details[0],
                'first_name': operator_details[1],
                'last_name': operator_details[2],
                'gender': operator_details[3],
                'phone': operator_details[7],
                'email': operator_details[4],
                'address': operator_details[6],
            }

        return render(request, 'edit_operator.html', {'operator': operator})





def time_slots(request):
    return render(request, 'manage_time_slots.html')









# Simulating booked time slots for each doctor
booked_time_slots = {
    "lujana": ["9:00 AM", "9:20 AM", "10:00 AM"],
    "dhiraj": ["9:40 AM", "10:20 AM", "11:00 AM"],
    "manoj": ["9:20 AM", "10:00 AM", "10:40 AM"],
}

def get_booked_time_slots(request, doctor):
    # Retrieve booked time slots for the specific doctor
    doctor_booked_slots = booked_time_slots.get(doctor, [])

    return JsonResponse({"booked_time_slots": doctor_booked_slots})

