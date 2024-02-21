from django.apps import AppConfig                                   # Importing the AppConfig class from django.apps module


class AccountsConfig(AppConfig):                                   # Defining the configuration for the 'accounts' app
    default_auto_field = 'django.db.models.BigAutoField'           # Setting the default auto-generated field to 'BigAutoField' for compatibility
    name = 'accounts'

    def ready(self):                                               # Defining a method 'ready' which is called when the application is prepared
        import accounts.signals                                    # Importing signals module from the accounts app from signal.py