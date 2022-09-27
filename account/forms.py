from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    # we must have a first name and last name
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    #  while some profile items have defaults, none are required
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    link1 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    link2 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)
    link3 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'address', 'link1', 'link2', 'link3']
