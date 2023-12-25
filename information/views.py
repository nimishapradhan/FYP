from django.shortcuts import render

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def terms(request):
    return render(request, 'terms.html')

def feedback(request):
    return render(request, 'feedback.html')