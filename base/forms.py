from django import forms
from django.forms import TextInput, FileInput
from .models import Image


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image')
        # widgets are required to give form components Bootstrap classes for styling
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'type': "text",
            }),
            'image': FileInput(attrs={
                'class': "form-control",
                'type': "file",
            }),
        }
