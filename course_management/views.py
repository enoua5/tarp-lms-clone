from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User

from course_management.forms import CourseForm
from .models import Course

# Create your views here.
def course_management(request):
    
    #current_user = request.user
    #course_list = Course.objects.all()
    try:        
        course_list = Course.objects.filter(instructor=request.user)
        return render(request, 'course_management/course_management.html', {'course_list' : course_list})
    except:
        return render(request, 'course_management/course_management.html', {})

def addCourse(request):
    form = CourseForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect('course_management:coursesMain')

    return render(request, 'course_management/course_form.html', {'form':form})
