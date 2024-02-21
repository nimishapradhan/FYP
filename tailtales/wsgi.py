"""
WSGI config for tailtales project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tailtales.settings')

application = get_wsgi_application()



#This code sets up the WSGI (Web Server Gateway Interface) application for a Django project.This WSGI application is what will be used to handle incoming HTTP requests and route them to the appropriate Django views and applications.The settings module contains configurations for the project such as database settings, installed apps, middleware, etc.In summary, this code sets up the WSGI application for a Django project by configuring the environment variable for the Django settings module and retrieving the WSGI application using get_wsgi_application().