# Django Imports
from django.shortcuts import render

# Our Imports
from .models import Course

# Course Dashboard
def dashboard(request):
    # Step 1: Get list of courses.
    course_list = Course.objects.all()

    # Step 2: Render our HTML page, passing it the list of courses
    return render(request, 'dashboard/dashboard.html', {'course_list' : course_list})