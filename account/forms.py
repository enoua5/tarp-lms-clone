from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}), required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    link1 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}))
    link2 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}))
    link3 = forms.URLField(max_length=200, widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['image', 'bio', 'address', 'link1', 'link2', 'link3']
