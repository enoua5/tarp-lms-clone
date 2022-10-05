from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User

from course_management.forms import CourseForm
from .models import Course


# Create your views here.
def course_management(request):
    try:        
        course_list = Course.objects.filter(instructor=request.user)
        return render(request, 'course_management/course_management.html', {'course_list' : course_list})
    except:
        return render(request, 'course_management/course_management.html', {})


def addCourse(request):
    form = CourseForm(request.POST or None)

    if form.is_valid():
        # I cannot believe that this was the solution. Hour count to approach this issue: at least 6
        # The problem was for the form to determine the current instructor automatically, without having 
        # a dropdown menu with all instructors showing up.
        course = form.save(commit=False)
        course.instructor = request.user
        course.save()
        return redirect('course_management:coursesMain')

    return render(request, 'course_management/course_form.html', {'form':form})


# Gets the id from the course_management.html template
def deleteCourse(request, id):
    toDelete = Course.objects.get(id=id)
    toDelete.delete()

    return redirect('course_management:coursesMain')


# Uses the same form as before.
def updateCourse(request, id):
    # Gets the course we are trying to update
    toUpdate = Course.objects.get(id=id)
    form = CourseForm(request.POST or None, instance=toUpdate)

    if form.is_valid():
        form.save()
        return redirect('course_management:coursesMain')

    return render(request, 'course_management/course_form.html', {'form':form, 'course':toUpdate})


# course page view
def coursePage(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'course_management/course_page.html', {'course': course, 'page_title': str(course)})


def addAssignment(request, id):
    course = Course.objects.get(id=id)
    # form stuff
    return render(request, 'course_management/assignment_management.html', {'course': course, 'page_title': str(course)})
