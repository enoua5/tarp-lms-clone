from django.shortcuts import render
from django.http import HttpResponse
from course_management.models import Course
from course_management.models import Assignment
from json import dumps
import json

# Create your views here.
def displaycalendar(request):
    try:
        # Create course list
        courses_list = None

        # Check if instructor or not.
        if request.user.groups.filter(name='Instructor').exists():
            courses_list = Course.objects.filter(instructor=request.user)
        else:
            courses_list = request.user.courses.all()

        # Grab the assignments attached to the courses and add to assignment_list
        assignment_list = Assignment.objects.none()
        a = 0
        for course in courses_list:
            assignment_list = assignment_list | Assignment.objects.filter(course_id=courses_list[a].id).select_related()
            a = a + 1

        assignment_title = []
        assignment_due = []

        c = 0
        for assignment in assignment_list:
            assignment_title.append(assignment_list[c].title)
            assignment_due.append(str(assignment_list[c].due_date.strftime("%Y-%m-%d %H:%M")))
            c = c + 1

        assignment_dict = {
            "titles": assignment_title,
            "dates": assignment_due
        }

        json_assignment_list = dumps(assignment_dict)

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

        return render(request, 'calendars/calendar.html', {'json_list': json_list,
                                                           'json_assignment_list': json_assignment_list,
                                                           'page_title': 'Calendar'})

    except:
        # Render without data if user isn't logged in.
        return render(request, 'calendars/calendar.html', {'page_title': 'Calendar'})