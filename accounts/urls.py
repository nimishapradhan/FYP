from django.urls import path, include
from accounts import views


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),

    path('do_register', views.do_register, name='do_register'),
    path('do_login', views.do_login, name='do_login'),
    path('logout', views.logout, name='logout'),
    path('feedback', views.feedback, name='feedback'),
    path('save_feedback', views.save_feedback, name='save_feedback'),

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_appointment_details', views.admin_appointment_details, name='admin_appointment_details'),
    path('admin_single_appointment/<id>', views.admin_single_appointment, name='admin_single_appointment'),
    path('admin_cancel_appointment/<id>', views.admin_cancel_appointment, name='admin_cancel_appointment'),
    path('admin_delete_appointment/<id>', views.admin_delete_appointment, name='admin_delete_appointment'),
    path('admin_profile', views.admin_profile, name='admin_profile'),
    path('admin_profile_update', views.admin_profile_update, name='admin_profile_update'),
    

    path('admin_payment_history', views.admin_payment_history, name='admin_payment_history'),
    path('admin_download_payment_history', views.admin_download_payment_history, name='admin_download_payment_history'),
    path('admin_payment_single_download/<id>', views.admin_payment_single_download, name='admin_payment_single_download'),

    path('admin_service_records', views.admin_service_records, name='admin_service_records'),
    path('admin_add_service', views.admin_add_service, name='admin_add_service'),
    path('admin_register_service', views.admin_register_service, name='admin_register_service'),
    path('admin_edit_service/<id>', views.admin_edit_service, name='admin_edit_service'),
    path('admin_update_service/<id>', views.admin_update_service, name='admin_update_service'),
    path('admin_delete_service/<id>', views.admin_delete_service, name='admin_delete_service'),
    path('admin_service_img_remove/<id>', views.admin_service_img_remove, name='admin_service_img_remove'),

    path('admin_patient_records', views.admin_patient_record, name='admin_patient_records'),
    path('admin_timeslots', views.admin_timeslots, name='admin_timeslots'),
    path('admin_add_timeslots', views.admin_add_timeslots, name='admin_add_timeslots'),
    path('admin_register_timeslots', views.admin_register_timeslots, name='admin_register_timeslots'),
    path('admin_edit_timeslots/<id>', views.admin_edit_timeslots, name='admin_edit_timeslots'),
    path('admin_update_timeslots/<id>', views.admin_update_timeslots, name='admin_update_timeslots'),
    path('admin_delete_timeslots/<id>', views.admin_delete_timeslots, name='admin_delete_timeslots'),

    path('admin_petowner_records', views.admin_petowner_record, name='admin_petowner_records'),
    path('admin_add_petowner', views.admin_add_petowner, name='admin_add_petowner'),
    path('admin_register_petowner', views.admin_register_petowner, name='admin_register_petowner'),
    path('admin_edit_petowner/<id>', views.admin_edit_petowner, name='admin_edit_petowner'),
    path('admin_update_petowner/<id>', views.admin_update_petowner, name='admin_update_petowner'),
    path('admin_delete_petowner/<id>', views.admin_delete_petowner, name='admin_delete_petowner'),
    path('admin_petowner_change_password/<id>', views.admin_petowner_change_password, name='admin_petowner_change_password'),

    path('admin_doctor_records', views.admin_doctor_record, name='admin_doctor_records'),
    path('admin_add_doctor', views.admin_add_doctor, name='admin_add_doctor'),
    path('admin_register_doctor', views.admin_register_doctor, name='admin_register_doctor'),
    path('admin_edit_doctor/<id>', views.admin_edit_doctor, name='admin_edit_doctor'),
    path('admin_update_doctor/<id>', views.admin_update_doctor, name='admin_update_doctor'),
    path('admin_delete_doctor/<id>', views.admin_delete_doctor, name='admin_delete_doctor'),
    path('admin_doctor_img_remove/<id>', views.admin_doctor_img_remove, name='admin_doctor_img_remove'),
    path('admin_doctor_change_password/<id>', views.admin_doctor_change_password, name='admin_doctor_change_password'),

    path('admin_operator_records', views.admin_operator_record, name='admin_operator_records'),
    path('admin_add_operator', views.admin_add_operator, name='admin_add_operator'),
    path('admin_register_operator', views.admin_register_operator, name='admin_register_operator'),
    path('admin_edit_operator/<id>', views.admin_edit_operator, name='admin_edit_operator'),
    path('admin_update_operator/<id>', views.admin_update_operator, name='admin_update_operator'),
    path('admin_delete_operator/<id>', views.admin_delete_operator, name='admin_delete_operator'),
    path('admin_operator_change_password/<id>', views.admin_operator_change_password, name='admin_operator_change_password'),

    path('admin_contact', views.admin_contact, name='admin_contact'),
    path('admin_contact_delete/<id>', views.admin_contact_delete, name='admin_contact_delete'),

    path('admin_feedback', views.admin_feedback, name='admin_feedback'),
    path('admin_feedback_delete/<id>', views.admin_feedback_delete, name='admin_feedback_delete'),

    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('user_appointment_list', views.user_appointment_list, name='user_appointment_list'),

    path('user_payment_list', views.user_payment_list, name='user_payment_list'),
    path('user_download_single_payment/<id>', views.user_download_single_payment, name='user_download_single_payment'),

    path('user_download_payment_all', views.user_download_payment_all, name='user_download_payment_all'),
    # path('user_generate_bill', views.user_generate_bill, name='user_generate_bill'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_profile_update', views.user_profile_update, name='user_profile_update'),
    path('user_change_password', views.user_change_password, name='user_change_password'),
    path('user_cancel_appointment/<id>', views.user_cancel_appointment, name='user_cancel_appointment'),
    path('user_appointment_detail/<id>', views.user_appointment_detail, name='user_appointment_detail'),


    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('all_appointments', views.doctor_all_appointment, name='doctor_all_appointments'),
    path('appointment_detail/<id>',views.doctor_single_appointment, name='doctor_single_appointment'),
    path('patient_details', views.doctor_patient_details, name='doctor_patient_details'),
    path('single_patient_details/<id>',views.doctor_single_patient, name='doctor_single_patient'),
    path('doctor_profile', views.doctor_profile, name='doctor_profile'),
    path('doctor_profile_update', views.doctor_profile_update, name='doctor_profile_update'),

    path('operator_dashboard', views.operator_dashboard, name='operator_dashboard'),
    path('operator_appointment_all', views.operator_appointment_all, name='operator_appointment_all'),
    path('operator_doctor', views.operator_doctor, name='operator_doctor'),
    path('operator_petowner', views.operator_petowner, name='operator_petowner'),
    path('operator_doctor_edit/<id>', views.operator_doctor_edit, name='operator_doctor_edit'),
    path('operator_doctor_change_status/<id>', views.operator_doctor_change_status, name='operator_doctor_change_status'),
    path('operator_petowner_details/<id>', views.operator_petowner_details, name='operator_petowner_details'),
    path('operator_profile', views.operator_profile, name='operator_profile'),

    path('initkhalti', views.initkhalti, name='initkhalti'),
    path('verifyKhalti', views.verifyKhalti, name='verifyKhalti'),

    path('khalti_request/<int:id>', views.khalti_request, name='khalti_request'),

    path('forget_password', views.forget_password, name='forget_password'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('reset_password', views.reset_password, name='reset_password'),
]