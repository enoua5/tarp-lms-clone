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
    # Step 0: Create hard-coded Instructors for testing, REMOVE LATER.
    if not Group.objects.get(name="Instructor"):
        Group.objects.create(name="Instructor")
        
    if not Group.objects.get(name="Student"):
        Group.objects.create(name="Student")
        
    ## Create test instructor.
    instructor_group = Group.objects.get(name="Instructor")
    test_instructor = User.objects.create_user(username='professor',
                                 email='professor@lms.com',
                                 password='admin')
    instructor_group.user_set.add(test_instructor)
    
    # Step 1.: Create hard-coded courses for testing, REMOVE LATER.
    cs3750 = Course.objects.get_or_create(
        department="CS",
        course_num=3750,
        course_name="Software Engineering II",
        instructor=test_instructor,
        meeting_days="M,W,F",
        # Datetime format: hour, minute, seconds
        meeting_start_time=datetime.time(9, 20, 0),
        meeting_end_time=datetime.time(10, 30, 0),
        meeting_location="NOORDA 304",
        credit_hours=4
    )
    
    net2420 = Course.objects.get_or_create(
        department="NET",
        course_num=2420,
        course_name="Networking I",
        instructor=test_instructor,
        meeting_days="T,Th",
        # Datetime format: hour, minute, seconds
        meeting_start_time=datetime.time(1, 20, 0),
        meeting_end_time=datetime.time(3, 30, 0),
        meeting_location="NOORDA 204",
        credit_hours=4
    )

    math3110 = Course.objects.get_or_create(
        department="MATH",
        course_num=3110,
        course_name="Statistics III",
        instructor=test_instructor,
        meeting_days="M,W,F",
        # Datetime format: hour, minute, seconds
        meeting_start_time=datetime.time(8, 20, 0),
        meeting_end_time=datetime.time(9, 30, 0),
        meeting_location="TH 310",
        credit_hours=3
    )

    phys2100 = Course.objects.get_or_create(
        department="PHSY",
        course_num=2100,
        course_name="Physics I",
        inst_name=test_instructor,
        meeting_days="T,Th",
        # Datetime format: hour, minute, seconds
        meeting_start_time=datetime.time(4, 30, 0),
        meeting_end_time=datetime.time(5, 20, 0),
        meeting_location="TH 402",
        credit_hours=5
    )

    # Step 2: Get list of courses that are under the currently authenticated instructor
    current_user = request.user
    course_list = Course.objects.get(username=current_user.username)

    # Step 2: Render our HTML page, passing it the list of courses
    return render(request, 'dashboard/dashboard.html', {'course_list' : course_list, 'page_title': "Dashboard"})
