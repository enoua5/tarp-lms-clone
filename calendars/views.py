from django.shortcuts import render
from django.http import HttpResponse
from course_management.models import Course
from json import dumps
import json

# Create your views here.
def displaycalendar(request):
    try:
        # Create course list
        courses_list = None

        # Check if instructor or not. If student give an empty list.
        if request.user.groups.filter(name='Instructor').exists():
            courses_list = Course.objects.filter(instructor=request.user)
        else:
            courses_list = []

        # Create two lists to store the course names and the meeting days.
        names = []
        times = []
        i = 0

        # Fill the lists.
        for course in courses_list:
            names.append(courses_list[i].department + str(courses_list[i].course_num))
            times.append(courses_list[i].meeting_days)
            i = i + 1

        # Place the lists in a dictionary.
        course_dict = {
            "course_name": names,
            "course_days": times
        }

        # Turn the dictionary into a json string.
        json_list = dumps(course_dict)

        return render(request, 'calendars/calendar.html', {'json_list': json_list, 'page_title': 'Calendar'})

    except:
        # Render without data if user isn't logged in.
        return render(request, 'calendars/calendar.html', {'page_title': 'Calendar'})