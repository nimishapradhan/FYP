from django.urls import path
from accounts import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

    path('do_register', views.do_register, name='do_register'),
    path('do_login', views.do_login, name='do_login'),
    path('logout', views.logout, name='logout'),

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_appointment_details', views.admin_appointment_details, name='admin_appointment_details'),

    path('admin_service_records', views.admin_service_records, name='admin_service_records'),
    path('admin_add_service', views.admin_add_service, name='admin_add_service'),
    path('admin_register_service', views.admin_register_service, name='admin_register_service'),
    path('admin_edit_service/<id>', views.admin_edit_service, name='admin_edit_service'),
    path('admin_update_service/<id>', views.admin_update_service, name='admin_update_service'),
    path('admin_delete_service/<id>', views.admin_delete_service, name='admin_delete_service'),

    path('admin_patient_records', views.admin_patient_record, name='admin_patient_records'),

    path('admin_petowner_records', views.admin_petowner_record, name='admin_petowner_records'),
    path('admin_add_petowner', views.admin_add_petowner, name='admin_add_petowner'),
    path('admin_register_petowner', views.admin_register_petowner, name='admin_register_petowner'),
    path('admin_edit_petowner/<id>', views.admin_edit_petowner, name='admin_edit_petowner'),
    path('admin_update_petowner/<id>', views.admin_update_petowner, name='admin_update_petowner'),
    path('admin_delete_petowner/<id>', views.admin_delete_petowner, name='admin_delete_petowner'),

    path('admin_doctor_records', views.admin_doctor_record, name='admin_doctor_records'),
    path('admin_add_doctor', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin_register_doctor', views.admin_register_doctor, name='admin_register_doctor'),
    path('admin_edit_doctor/<id>', views.admin_edit_doctor, name='admin_edit_doctor'),
    path('admin_update_doctor/<id>', views.admin_update_doctor, name='admin_update_doctor'),
    path('admin_delete_doctor/<id>', views.admin_delete_doctor, name='admin_delete_doctor'),

    path('admin_operator_records', views.admin_operator_record, name='admin_operator_records'),
    path('admin_add_operator', views.admin_add_operator, name='admin_add_operator'),
    path('admin_register_operator', views.admin_register_operator, name='admin_register_operator'),
    path('admin_edit_operator/<id>', views.admin_edit_operator, name='admin_edit_operator'),
    path('admin_update_operator/<id>', views.admin_update_operator, name='admin_update_operator'),
    path('admin_delete_operator/<id>', views.admin_delete_operator, name='admin_delete_operator'),

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