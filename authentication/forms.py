from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    birthday=forms.DateField(label='birthday')

    class Meta:
        model = get_user_model() 
        
        fields = ['username','email', 'first_name','last_name','birthday','password1', 'password2']
