from attr import attributes
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from .models import Course

DAYS_OF_WEEK = [
    ('Monday', 'M'),
    ('Tuesday', 'T'),
    ('Wednesday', 'W'),
    ('Thursday', 'Th'),
    ('Friday', 'Fr')
]

class CourseForm(ModelForm):
    class Meta:
        model = Course 
        exclude = ['instructor']

        # We can change the labels for anything!
        labels = {
        "course_num":  "Course number"
        }

        # This is where the pretty magic comes in!!
        widgets = {
            "department": forms.TextInput(attrs={'placeholder': 'Department', 'id':"department", 'class': 'form-control'}),
            "course_num": forms.NumberInput(attrs={'id':"course_num",'placeholder': 0, 'class': 'form-control'}),
            "course_name": forms.TextInput(attrs={'id':"course_name",'placeholder': 'Course Name', 'class': 'form-control'}),
            "meeting_days": forms.CheckboxSelectMultiple(choices=DAYS_OF_WEEK),
            "meeting_start_time": forms.TimeInput(attrs={'id':"meeting_start_time",'type': 'time', 'class': 'form-control'}),
            "meeting_end_time": forms.TimeInput(attrs={'id':"meeting_end_time",'type': 'time', 'class': 'form-control'}),
            "meeting_location": forms.TextInput(attrs={'id':"meeting_location",'placeholder': 'TBA', 'class': 'form-control'}),
            "credit_hours":forms.NumberInput(attrs={'id':"credit_hours",'class': 'form-control'})
        }

        error_messages = {
        'meeting_days': {
            'required': ("Please enter meeting days"),
           },
        }

        # Just to remember the fields
        # fields = ["course_num", "department", "course_name", 
        #           "meeting_days", "meeting_start_time", "instructor",
        #           "meeting_end_time", "meeting_location", "credit_hours"]
        

