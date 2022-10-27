from django import forms
from django.forms import ModelForm, ValidationError
from .models import Course, Assignment, Submission, FileSubmission, TextSubmission

# ------------------ COURSE MANAGEMENT ------------------

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
        exclude = ['instructor', 'students']

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
            "credit_hours":forms.NumberInput(attrs={'id':"credit_hours",'class': 'form-control'}),
            "a_threshold":forms.NumberInput(attrs={'id':"a_threshold", 'class': 'form-control'}),
            "increment":forms.NumberInput(attrs={'id':"increment", 'class': 'form-control'})
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


# ------------------ ASSIGNMENT MANAGEMENT ------------------

# the following 2 classes are required to ensure that the html datetime-local type plays nicely with the django form
# code from https://www.davidjabb.com/blog/2021/12/1/how-to-use-the-built-in-html-datetime-local-widget-in-a-django-form/
# if we need to change this I will cry  ~ Daniel
class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"


class DateTimeLocalField(forms.DateTimeField):
    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N
    # is True, the locale-dictated format will be applied
    # instead of settings.DATETIME_INPUT_FORMATS.

    input_formats = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M", attrs={'class': 'form-control'})


class AssignmentForm(ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=True)
    due_date = DateTimeLocalField()
    points = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    type = forms.ChoiceField(choices=(('t', 'Text entry'), ('f', 'File upload')), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Assignment
        exclude = ['course']


class FileSubmissionForm(ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}), required=True)

    class Meta:
        model = FileSubmission
        exclude = ['assignment', 'student', 'score']


class TextSubmissionForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 15}), required=True)

    class Meta:
        model = TextSubmission
        exclude = ['assignment', 'student', 'score']


class GradeSubmissionForm(ModelForm):
    score = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Submission
        fields = ['score']

    # validate score is under max score
    # no need to validate score is positive because score is a positive integer field, validation is automatic
    def clean(self):
        cd = super().clean()
        score_input = cd.get('score')

        if score_input:
            if not score_input <= self.instance.assignment.points:
                raise ValidationError("Ensure this value is less than or equal to the maximum assignment points.")
            return cd
