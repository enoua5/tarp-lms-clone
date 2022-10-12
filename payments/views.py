from django.shortcuts import render
from course_management.models import Course
from django.contrib.auth.models import Group
from .models import Tuition

# Create your views here.
def tuition(request):
    # A precaution, in case student/course relationship does not exist
    try:        
        course_list = request.user.courses.all()
        balance = Tuition.objects.get(user=request.user).balance

        return render(request, 'payments/tuition_page.html', {'course_list' : course_list, 'balance' : balance})
    except:  
        return render(request, 'payments/tuition_page.html', {'course_list' : {}})

