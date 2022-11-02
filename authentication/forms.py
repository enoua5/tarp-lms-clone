from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

ACCOUNT_TYPES = [
    ('student', 'Student'),
    ('instructor', 'Instructor'),
]


class RegistrationForm(UserCreationForm):
    birthdate = forms.DateField(required=True, widget=forms.NumberInput(attrs={'type': 'date', 'id': 'birthdate'}))
    account_type = forms.CharField(label='Choose the account type', widget=forms.Select(choices=ACCOUNT_TYPES))

    # Loops through fields and adds a bootsrap form-control class
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values() :
            field.widget.attrs["class"] = "form-control"
        
        # Adding labels and ids to make things pretty
        self.fields['password1'].label = "Create a password"
        self.fields['password2'].label = "Confirm a password"
        self.fields['password1'].widget.attrs.update({'id': 'password1', 'placeholder':'password'})
        self.fields['password2'].widget.attrs.update({'id': 'password2', 'placeholder':'password'})


    # Used the clean method to validate if the user
    # signing up is old enough
    def clean(self):
        cd = super().clean()

        date = cd.get("birthdate")

        # Checks if the date is in a valid format
        if date:
            d = datetime.date.today()
            oldEnough = datetime.timedelta(days=6574)

            # Calculates the difference in days between now
            # and the date user entered.
            diff = d - date

            # Compares this difference to the value of 18 years
            if diff.days < oldEnough.days:
                raise ValidationError("You have to be 18 or older to sign up.")

            return cd

    class Meta:
        model = User 
        
        fields = ['username', 'email', 'first_name', 'last_name', 'birthdate', 'password1', 'password2', 'account_type']

        labels = {
            "username":  "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
        }
        
        widgets = {
            "username": forms.TextInput(attrs={'placeholder': 'username', 'id':"username"}),
            "email": forms.EmailInput(attrs={'id':"email", 'placeholder': 'email@email.com'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'John','id':'first_name'}),
            "last_name": forms.TextInput(attrs={'id':"last_name", 'placeholder': 'Doe'}),
        }

class LoginForm(AuthenticationForm):
    # Loops through fields and adds a bootsrap form-control class
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values() :
            field.widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs.update({'id': 'username'})
        self.fields['password'].widget.attrs.update({'id': 'password'})

    class Meta:
        model = User 
        
        fields = ['username', 'password']