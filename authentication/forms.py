from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime

class RegistrationForm(UserCreationForm):
    birthday=forms.DateField(label='birthday', required=True)

    # Used the clean method to validate if the user
    # signing up is old enough
    def clean(self):
        cd = super().clean()

        date = cd.get("birthday")

        # Checks if the date is in a valid format
        if(date):
            d = datetime.date.today()
            oldEnough = datetime.timedelta(days=6574)

            # Calculates the difference in days between now
            # and the date user entered.
            diff = d - date

            # Compares this difference to the value of 18 years
            if diff.days < oldEnough.days:
                print(diff.days < oldEnough.days)
                raise ValidationError("You have to be 18 or older to sign up.")
            
            return cd

    class Meta:
        model = get_user_model() 
        
        fields = ['username','email', 'first_name','last_name','birthday','password1', 'password2']
