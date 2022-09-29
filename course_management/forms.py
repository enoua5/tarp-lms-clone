from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from psutil import users
from .models import Course

DAYS_OF_WEEK = [
    ('m', 'M'),
    ('t', 'T'),
    ('w', 'W'),
    ('th', 'Th'),
    ('fr', 'Fr')
]

class CourseForm(ModelForm):
    class Meta:
        model = Course 
        #exclude = ['instructor']
        labels = {
        "course_num":  "Course number"
        }
        # widgets = {
        #     "meeting_days": forms.CheckboxSelectMultiple(choices=DAYS_OF_WEEK)
        # }

        fields = ["course_num", "department", "course_name", 
                  "meeting_days", "meeting_start_time", "instructor",
                  "meeting_end_time", "meeting_location", "credit_hours"]
