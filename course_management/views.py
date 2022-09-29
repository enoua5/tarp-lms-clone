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

    # Step 1: Get list of courses that are under the currently authenticated instructor
    try:        
        course_list = Course.objects.get(instructor=request.user)
        return render(request, 'course_management/course-management.html', {'course_list' : course_list})
    except:
        # This will run if the currently logged in user doesn't have any courses, or isn't logged in.
        return render(request, 'course_management/course-management.html', {})
    