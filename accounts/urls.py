from django.urls import path
from accounts import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

    path('do_register', views.do_register, name='do_register'),
    path('do_login', views.do_login, name='do_login'),
    path('logout', views.logout, name='logout'),

    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('user_appointment_list', views.user_appointment_list, name='user_appointment_list'),
    path('user_payment_list', views.user_payment_list, name='user_payment_list'),
    path('user_generate_bill', views.user_generate_bill, name='user_generate_bill'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_profile_update', views.user_profile_update, name='user_profile_update'),
    path('user_change_password', views.user_change_password, name='user_change_password'),


    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('all_appointments', views.doctor_all_appointment, name='doctor_all_appointments'),
    path('appointment_detail/<id>',views.doctor_single_appointment, name='doctor_single_appointment'),
    path('patient_details', views.doctor_patient_details, name='doctor_patient_details'),
    path('single_patient_details/<id>',views.doctor_single_patient, name='doctor_single_patient'),
    path('doctor_profile', views.doctor_profile, name='doctor_profile'),
    path('doctor_profile_update', views.doctor_profile_update, name='doctor_profile_update'),
]