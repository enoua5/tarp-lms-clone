# Python Imports
import datetime

# Django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Our Imports
from course_management.models import Course

# Course Dashboard
def dashboard(request):    
    # Get list of courses that are under the currently authenticated user.
    try:        
        # Check if user is an instructor or user
        if request.user.groups.filter(name='Instructor').exists():
            course_list = Course.objects.filter(instructor=request.user)
        else:
            course_list = request.user.courses.all()
            
        return render(request, 'dashboard/dashboard.html', {'course_list' : course_list, 'page_title': "Dashboard"})
    except:
        # This will run if the currently logged in user doesn't have any courses, or isn't logged in.
        return render(request, 'dashboard/dashboard.html', {'page_title': "Dashboard"})
        

    # Step 2: Render our HTML page, passing it the list of courses
    
