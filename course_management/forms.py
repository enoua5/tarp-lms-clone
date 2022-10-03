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
        labels = {
        "course_num":  "Course number"
        }

        widgets = {
            "department": forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            "course_num": forms.NumberInput(attrs={'placeholder': 0, 'class': 'form-control'}),
            "course_name": forms.TextInput(attrs={'placeholder': 'Course Name', 'class': 'form-control'}),
            "meeting_days": forms.CheckboxSelectMultiple(choices=DAYS_OF_WEEK),
            "meeting_start_time": forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }

        error_messages = {
        'meeting_days': {
            'required': ("Please enter meeting days"),
           },
        }

        attrs = {
        'course_num': {
            'class': "form-control",
           },
        }
        # fields = ["course_num", "department", "course_name", 
        #           "meeting_days", "meeting_start_time", "instructor",
        #           "meeting_end_time", "meeting_location", "credit_hours"]
        

