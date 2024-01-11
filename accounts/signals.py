from django.db.models.signals import post_save
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=UserSocialAuth)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.provider == 'google-oauth2':
            instance.user.is_patient = True
            instance.user.save()