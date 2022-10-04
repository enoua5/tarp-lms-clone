# Python Imports
import datetime

# Django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Our Imports
from course_management.models import Course

# Course Dashboard
@login_required
def dashboard(request):
    # Step 0: Create hard-coded Instructors for testing, REMOVE LATER.
    instructor_group, already_created = Group.objects.get_or_create(name="Instructor")
    test_instructor = None
    try:
        test_instructor = User.objects.get(username='professor')
    except:
        test_instructor = User.objects.create(username='professor', first_name="Professor", last_name="Bean")
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
        instructor=test_instructor,
        meeting_days="T,Th",
        # Datetime format: hour, minute, seconds
        meeting_start_time=datetime.time(4, 30, 0),
        meeting_end_time=datetime.time(5, 20, 0),
        meeting_location="TH 402",
        credit_hours=5
    )
    
    # Create test student (REMOVE LATER).
    student_group, already_created = Group.objects.get_or_create(name="Student")
    test_student = None
    try:
        test_student = User.objects.get(username='student')
    except:
        test_student = User.objects.create(username='student', first_name="Nerdy", last_name="McNerd")
        student_group.user_set.add(test_student)
    
    cs3750[0].students.add(test_student)
    math3110[0].students.add(test_student)
    
    # Step 2: Get list of courses that are under the currently authenticated user.
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
    
