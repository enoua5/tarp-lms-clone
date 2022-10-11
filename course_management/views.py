from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from course_management.forms import CourseForm, AssignmentForm, FileSubmissionForm, TextSubmissionForm
from .models import Course, Assignment, FileSubmission, TextSubmission

# A view of courses for instructors
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

# A view of courses for students
def studentCourses(request):
        # A precaution, if the student/course relationship does not exist
        try:        
            my_course_list = request.user.courses.all()
            all_course_list = Course.objects.all().exclude(students=request.user)
            return render(request, 'course_management/student_courses.html', {'my_course_list' : my_course_list, 'all_course_list' : all_course_list})
        except:
            all_course_list = Course.objects.all().exclude(students=request.user)
            return render(request, 'course_management/student_courses.html', {'all_course_list' : all_course_list})

# Allows a student to register for a course
def register(request, id):
    toRegister = Course.objects.get(id=id)
    toRegister.students.add(request.user)
    return redirect('course_management:studentCourses')

# Allows a student to drop a course
def drop(request, id):
    toDrop = Course.objects.get(id=id)
    toDrop.students.remove(request.user)
    return redirect('course_management:studentCourses')

# course page view
def coursePage(request, id):
    course = Course.objects.get(id=id)
    assignment_list = Assignment.objects.filter(course=course)
    return render(request, 'course_management/course_page.html', {'course': course, 'page_title': str(course), 'assignment_list': assignment_list})
    
def addAssignment(request, id):
    course = Course.objects.get(id=id)

    # form stuff
    form = AssignmentForm(request.POST or None)
    if form.is_valid():
        assignment = form.save()
        assignment.course = course
        assignment.save()
        return redirect('course_management:coursePage', id)

    return render(request, 'course_management/assignment_form.html', {'course': course, 'page_title': str(course), 'form': form})


def assignmentSubmission(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == 'POST':
        # form will be different depending on the submission type
        if assignment.type == 'f':
            # if there is already a submission, pass it as the instance
            current_submission = FileSubmission.objects.filter(assignment=assignment, student=request.user).first()
            if current_submission:
                form = FileSubmissionForm(request.POST, request.FILES, instance=current_submission)
            else:
                form = FileSubmissionForm(request.POST)
        else:
            # if there is already a submission, pass it as the instance
            current_submission = TextSubmission.objects.filter(assignment=assignment, student=request.user).first()
            if current_submission:
                form = TextSubmissionForm(request.POST, instance=current_submission)
            else:
                form = TextSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('course_management:coursePage', course_id)
    else:
        if assignment.type == 'f':
            form = FileSubmissionForm()
            return render(request, 'course_management/assignment_submission.html',
                          {'course': course, 'assignment': assignment, 'path_title': str(assignment), 'form': form})
        else:
            form = TextSubmissionForm()
            return render(request, 'course_management/assignment_submission.html',
                          {'course': course, 'assignment': assignment, 'path_title': str(assignment), 'form': form})

