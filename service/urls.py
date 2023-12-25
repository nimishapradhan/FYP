from django.urls import path
from service import views


urlpatterns = [
    path('', views.service, name='service'),

    path('appointment_booking', views.appointment_booking, name='appointment_booking'),
    path('do_appointment_booking', views.do_appointment_booking, name='do_appointment_booking'),

]