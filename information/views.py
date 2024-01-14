from django.shortcuts import render, redirect
from django.contrib import messages
from information.models import Contact
from django.http import HttpResponseRedirect
from accounts.models import Doctor
from service.models import Service
from tailtales.settings import MEDIA_URL
# Create your views here.

def index_view(request):
    doctor = Doctor.objects.filter(status = True)[:3]
    service = Service.objects.filter(status = True)[:3]

    return render(request, 'index.html', {'doctor':doctor, 'service':service, 'MEDIA_URL':MEDIA_URL})

def about(request):
    return render(request, 'about.html')

def team(request):
    doctor = Doctor.objects.filter(status = True)
    return render(request, 'team.html', {'doctor':doctor, 'MEDIA_URL':MEDIA_URL})

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def terms(request):
    return render(request, 'terms.html')

# Define a function named save_contact that takes a request object as an argument
def save_contact(request):
     # Check if the request method is 'POST':  The POST request method requests that a web server accept the data enclosed in the body of the request message, most likely for storing it.
    if request.method == 'POST':
        # Retrieve form data from the POST request
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        phone = request.POST['phone']
        notes = request.POST['notes']

        # Check if a contact with the same email and phone already exists in the Contact model
        if Contact.objects.filter(email=email, phone=phone):
             # If the contact already exists, display a success message and redirect back to the previous page
            messages.success(request, 'You have already contacted us.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
      # If the contact doesn't exist, create a new Contact object and save it to the database
        contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone, notes=notes)
        contact.save()

      # Display a success message and redirect back to the previous page
        messages.success(request, 'Thank you for contacting us. We will get back to you shortly!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    