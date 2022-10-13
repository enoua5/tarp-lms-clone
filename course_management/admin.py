from django.contrib import admin
from .models import Course, Assignment, FileSubmission, TextSubmission

# Register your models here.
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(FileSubmission)
admin.site.register(TextSubmission)
