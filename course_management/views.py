from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Course

# Create your views here.
def course_management(request):

    current_user = request.user
    course_list = Course.objects.all()

    course_list = {}
    context = {
        'course_list': course_list,
    }

    return render(request, 'course_management/course-management.html', context)
