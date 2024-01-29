from django.db.models.signals import post_save                              # Importing signal for post-save operation.
from django.dispatch import receiver                                        # Importing receiver decorator for signal handling.
from social_django.models import UserSocialAuth                             # Importing UserSocialAuth model from social_django app.
from django.contrib.auth import get_user_model                               # Importing get_user_model function for fetching the User model.

User = get_user_model()                                                      #Fetching the User model dynamically.

@receiver(post_save, sender=UserSocialAuth)                                   # Registering a receiver for the post-save signal of UserSocialAuth model.
def update_user_profile(sender, instance, created, **kwargs):                 #It is triggered after a UserSocialAuth instance is saved.
    if created:                                                               #checks if the UserSocialAuth instance was just created (created) and if its provider is 'google-oauth2'
        if instance.provider == 'google-oauth2':
            instance.user.is_patient = True                                      #Set the is_patient attribute for user instance.
            instance.user.save()                                                 #Saving the updated user to db.