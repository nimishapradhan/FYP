from django import forms

class PetOwnerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    password = forms.CharField(widget=forms.PasswordInput())
    address = forms.CharField(widget=forms.Textarea)





