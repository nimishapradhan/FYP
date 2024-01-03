def set_is_patient(strategy, details, user=None, is_new=False, *args, **kwargs):
    # Check if the user is logging in with Google
    if strategy.backend.ModelBackend == 'google-oauth2' and is_new:
        # Set is_patient to True for the user
        user.is_patient = True
        user.save()