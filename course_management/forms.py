from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelForm
from psutil import users
from .models import Course

DAYS_OF_WEEK = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]
class CourseForm(ModelForm):
    #geeks_field = forms.CharField(label = "New Geeks Field")

    class Meta:
        model = Course 
        exclude = ['instructor']
        labels = {
        "course_num":  "Course number",
        "new_password1": "new_pw_label",
        "new_password2": "new_pw_label2",
        }


        widgets = {
            "meeting_days": forms.CheckboxSelectMultiple(choices=DAYS_OF_WEEK)
        }

        # fields = ["course_num", "department", "course_name", 
        #           "meeting_days", "meeting_start_time", 
        #           "meeting_end_time", "meeting_location", "credit_hours"]

# class CourseForm(forms.Form):
#     department = forms.CharField(max_length=4)
#     course_num = forms.IntegerField()
#     course_name = forms.CharField(max_length=100)
#     meeting_days = forms.CharField(empty_value="M,W,F", max_length=10)
#     meeting_start_time = forms.TimeField()
#     meeting_end_time = forms.TimeField()
#     meeting_location = forms.CharField(max_length=25, empty_value="TBA")
#     credit_hours = forms.IntegerField()

    # title = forms.CharField(
    #     max_length=3,
    #     widget=forms.Select(choices=TITLE_CHOICES),
    # )