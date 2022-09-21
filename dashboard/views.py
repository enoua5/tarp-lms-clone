# Django Imports
from django.shortcuts import render

# Our Imports
from .models import Course

# Course Dashboard
def dashboard(request):
    # Step 0: Create hard-coded courses for testing, REMOVE LATER.
    cs3750 = Course.objects.get_or_create(
        department="CS",
        course_num=3750,
        course_name="Software Engineering II",
        inst_name="Arpit Christi",
        meeting_time="T/TH 9:30-11:20AM",
        meeting_location="NOORDA 304"
    )

    net2420 = Course.objects.get_or_create(
        department="NET",
        course_num=2420,
        course_name="Networking I",
        inst_name="Brad Monte",
        meeting_time="M/W/F 9:30-10:20AM",
        meeting_location="NOORDA 204"
    )

    math3110 = Course.objects.get_or_create(
        department="MATH",
        course_num=3110,
        course_name="Statistics III",
        inst_name="Julian Chan",
        meeting_time="M/W/F 11:30-12:20PM",
        meeting_location="TH 310"
    )

    phys2100 = Course.objects.get_or_create(
        department="PHSY",
        course_num=2100,
        course_name="Physics I",
        inst_name="Marie Elsworth",
        meeting_time="T/Th 1:30-2:20PM",
        meeting_location="TH 402"
    )

    # Step 1: Get list of courses.
    course_list = Course.objects.all()

    # Step 2: Render our HTML page, passing it the list of courses
    return render(request, 'dashboard/dashboard.html', {'course_list' : course_list})