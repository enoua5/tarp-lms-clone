from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    # we must have a first name and last name
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    #  while some profile items have defaults, none but birthdate are required
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'image'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id': 'bio'}), required=False)
    address_line1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address_line1'}), required=False)
    address_line2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address_line2'}), required=False)
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}), required=False)
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'state'}), required=False)
    zip = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'zip'}), required=False)
    birthdate = forms.DateField(required=True)
    link1 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'id': 'link1'}), required=False)
    link2 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'id': 'link2'}), required=False)
    link3 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control', 'id': 'link3'}), required=False)

    class Meta:
        model = Profile
        exclude = ['user']
