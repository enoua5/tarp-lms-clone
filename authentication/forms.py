from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    birthday=forms.DateField(label='birthday')

    # def clean(self):
    #     cd = self.cleaned_data

    #     password1 = cd.get("password1")
    #     password2 = cd.get("password2")

    #     if password1 != password2:
    #         #Or you might want to tie this validation to the password1 field
    #         raise ValidationError("Passwords did not match")


    #return cd
    class Meta:
        model = get_user_model() 
        
        fields = ['username','email', 'first_name','last_name','birthday','password1', 'password2']
