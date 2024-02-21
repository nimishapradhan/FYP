"""tailtales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin                       #functionality related to the Django administration site
from django.urls import path, include                   #imports the path function and the include function from the django.urls package for defining URL patterns 
from django.conf.urls.static import static               #used to serve static files (such as CSS, JavaScript, and images)
from tailtales import settings                            #imports the settings module that contains project-specific settings 
from information import views                               # imports the views module from the information app

urlpatterns = [
    path('admin/', admin.site.urls),                 #Django ko built-in admin interface
    path('', views.index_view, name='index'),        #index_view function in the views.py file of the information app , '' represents the root URL
    path('', include('information.urls')),         #include URLs from another URL configuration module(information)
    path('service/', include('service.urls')),    #service app's urls ko path
    path('user/', include('accounts.urls')),        #account app's urls path
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    #static files of media
