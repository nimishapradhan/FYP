from django.urls import path
from . import views


from django.urls import path, include


urlpatterns = [
    path('', views.index_view, name='index'),  # Maps to the index_view function for the path '/index/'
    path('about', views.about_view, name='about'),  # Maps to the about_view function for the path '/about/'
    path('service', views.service_view, name='service'),  
    path('team', views.team_view, name='team'),  
    path('contact', views.contact_view, name='contact'),  
    path('faq', views.faq_view, name='faq'),  
    path('feedback', views.feedback_view, name='feedback'),  
    path('terms', views.terms_view, name='terms'),  
    path('payment', views.payment_view, name='payment'),  
    path('booking', views.booking_view, name='booking'),
    path('password', views.password_view, name='password'), 
    path('passwordreset', views.passwordreset_view, name='passwordreset'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('reset_password', views.reset_password, name='reset_password'),


    path('admin_login', views.admin_login , name = 'admin_login'),
    path('login/', views.login_view, name='login'),  
    path('register/', views.register_view, name='register'),
    path('doc_register', views.doc_register_view, name='doc_register'),

    
    path('admin_nav', views.adminnav_view, name='admin_nav'), 
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'), 
    path('admin_doctor', views.admin_doctor_view, name='admin_doctor'), 
    path('admin_patient', views.admin_patient_view, name='admin_patient'), 
    path('admin_app', views.admin_app_view, name='admin_app'), 
    path('admin_payment', views.admin_payment_view, name='admin_payment'), 
    path('admin_service', views.admin_service_view, name='admin_service'), 
    path('admin_operator', views.admin_operator, name='admin_operator'), 
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('admin_cancelled_appointment', views.admin_cancelled_appointment, name='admin_cancelled_appointment'), 



    path('delete_operator/<int:operator_id>/', views.delete_operator, name='delete_operator'),
    path('edit_operator/<int:operator_id>/', views.edit_operator, name='edit_operator'),


   # Add a URL pattern for edit_doctor_admin
    path('edit_doctor_admin/<int:doctor_id>/', views.edit_doctor_admin, name='edit_doctor_admin'),

    path('delete_doctor_admin/<int:doctor_id>/', views.delete_doctor_admin, name='delete_doctor_admin'),
   



   


    path('oappointment', views.oappointment_view, name='oappointment'),
    path('odashboard', views.odashboard, name='odashboard'), 
    path('odoctor', views.odoctor, name='odoctor'), 
    path('opatient', views.opatient, name='opatient'), 
    path('oprofile', views.oprofile, name='oprofile'), 
    path('oprofile', views.oprofile, name='oprofile'), 
    path('operator_register', views.operator_register_view, name='operator_register'),




    path('user_nav', views.usernav_view, name='user_nav'),  
    path('user_dashboard', views.userdashboard_view, name='user_dashboard'),  
    path('user_app', views.userapp_view, name='user_app'),  
    path('user_payment', views.userpayment_view, name='user_payment'),  
    path('user_profile', views.userprofile_view, name='user_profile'), 
    path('user_history', views.uhistory_view, name='user_history'),  


    path('doctordash_main', views.doctordashmain_view, name='doctordash_main'),  
    path('doctor_profile', views.doctorprofile_view, name='doctor_profile'),  
    path('doctor_patient', views.doctorpatient_view, name='doctor_patient'),  
    path('doctorapp', views.doctorapp_view, name='doctorapp'),  
    path('doctornav', views.doctornav_view, name='doctornav'),
    path('xyz', views.xyz_view, name='xyz'),
    path('invoice', views.invoice_view, name='invoice'),
    path('timeslots', views.time_slots, name='timeslots'),
    path('logout/', views.logout_view, name='logout'),


    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
    path('delete_appointment_doc/', views.delete_appointment_doc, name='delete_appointment_doc'),
    path('delete_appointment_admin/', views.delete_appointment_admin, name='delete_appointment_admin'),
    path('delete_patient_admin/', views.delete_patient_admin, name='delete_patient_admin'),

 

   
    path('get_booked_time_slots/<str:doctor>/', views.get_booked_time_slots, name='get_booked_time_slots'),




]
    
