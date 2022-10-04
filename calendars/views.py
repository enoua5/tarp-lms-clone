from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def displaycalendar(request):
    return render(request, 'calendars/calendar.html', {'page_title': 'Calendar'})