from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime

ACCOUNT_TYPES = [
    ('student', 'Student'),
    ('instructor', 'Instructor'),
]


class RegistrationForm(UserCreationForm):
    birthdate = forms.DateField(label='birthdate', required=True)
    account_type = forms.CharField(label='role', widget=forms.Select(choices=ACCOUNT_TYPES))

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
        model = get_user_model() 
        
        fields = ['username', 'email', 'first_name', 'last_name', 'birthdate', 'password1', 'password2', 'account_type']
