from django.shortcuts import render
from django.http import HttpResponse
from course_management.models import Course
from json import dumps

# Create your views here.
def displaycalendar(request):
    courses_list = Course.objects.all()

    return render(request, 'calendars/calendar.html', {'course_list' : courses_list, 'page_title': 'Calendar'})