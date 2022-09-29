from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group

# Create your views here.
def course_management(request):
    context = {}
    return render(request, 'course_management/course-management.html', context)
