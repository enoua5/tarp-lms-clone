# Python Imports
import datetime

# Django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Our Imports
from course_management.models import Course

# Our Views
@login_required
def dashboard(request):    
    # Get list of courses that are under the currently authenticated user.
    try:        
        # Check if user is an instructor or user.
        if request.user.groups.filter(name='Instructor').exists():
            course_list = Course.objects.filter(instructor=request.user)
        else:
            # User is a student.
            course_list = request.user.courses.all()
            grade_list = list(map(lambda course: course.getStudentGrade(request.user), course_list))
            course_grade_list = zip(course_list, grade_list)
            assignments = []
            if course_list is not None:
                assignments = getNextAssignments(request.user)
                
            # Don't pass assignments if the user doesn't have any.
            if len(assignments) != 0:
                return render(request, 'dashboard/dashboard.html', {'course_grade_list': course_grade_list,
                                                                    'page_title': "Dashboard",
                                                                    'assignments': assignments})
                
        # This will run for students that don't have assignments, and for instructors.
        return render(request, 'dashboard/dashboard.html', {'course_list' : course_list,
                                                            'page_title': "Dashboard"})
    except:
        # This will run if the currently logged in user doesn't have any courses, or isn't logged in.
        return render(request, 'dashboard/dashboard.html', {'page_title': "Dashboard"})
        
        
# Supporting Functions
'''!
    @brief Gets the student's next 5 assignments to do.
    @details This function filters out any assignments that are overdue.
    @param student_user The user object that corresponds to the target student.
    @return assignment_list The list of Assignment objects that are assigned to
                            the student.
'''
def getNextAssignments(student_user):
    assignment_list = []
    course_list = student_user.courses.all()
    for course in course_list:
        # Get list of assignments from all of the student's courses...
        course_assignments = course.assignments.all()
        # ... and filter out those that are already overdue.
        for assignment in course_assignments:
            if not assignment.overdue():
                assignment_list.append(assignment)
    
    # Filter assigment list down to first 5, if possible
    if len(assignment_list) > 0:
        assignment_list.sort(key=lambda assignment: assignment.due_date)
        assignment_list = (assignment_list)[:5]
        
    return assignment_list
