from django.urls import path
from information import views


urlpatterns = [
    path('about', views.about, name='about'),
    path('team', views.team, name='team'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('terms', views.terms, name='terms'),
    path('save_contact', views.save_contact, name='save_contact'),
]