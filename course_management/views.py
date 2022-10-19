from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Course, Assignment, Submission, FileSubmission, TextSubmission
from payments.models import Tuition
from course_management.forms import CourseForm, AssignmentForm, FileSubmissionForm, TextSubmissionForm

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
            all_instructors_list = User.objects.filter(groups__name='Instructor')
            return render(request, 'course_management/student_courses.html', {'my_course_list' : my_course_list, 'all_course_list' : all_course_list, 'all_instructors_list': all_instructors_list})
        except:
            all_course_list = Course.objects.all().exclude(students=request.user)
            all_instructors_list = User.objects.filter(groups__name='Instructor')
            return render(request, 'course_management/student_courses.html', {'all_course_list' : all_course_list, 'all_instructors_list': all_instructors_list})

# Allows a student to register for a course
def register(request, id):
    toRegister = Course.objects.get(id=id)
    toRegister.students.add(request.user)

    # Now, we put a student into cellege debdt. STONKS 
    student_tuition = Tuition.objects.get(user=request.user)
    student_tuition.balance += 100*toRegister.credit_hours
    student_tuition.save()

    return redirect('course_management:studentCourses')

# Allows a student to drop a course
def drop(request, id):
    toDrop = Course.objects.get(id=id)
    toDrop.students.remove(request.user)

    # We need to refund the class fee
    student_tuition = Tuition.objects.get(user=request.user)
    student_tuition.balance -= 100*toDrop.credit_hours
    student_tuition.save()

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
        assignment = form.save(commit=False)
        assignment.course = course
        assignment.save()
        return redirect('course_management:coursePage', id)

    return render(request, 'course_management/assignment_form.html', {'course': course, 'page_title': str(course), 'form': form})


# assignment submission view - distinguishes between file and text submission
def assignmentSubmission(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)

    if assignment.type == 'f':
        # get current submission, pass it as an instance if it exists
        current_submission = FileSubmission.objects.filter(assignment=assignment).filter(student=request.user).first()
        if current_submission:
            form = FileSubmissionForm(request.POST or None, instance=current_submission)
        else:
            form = FileSubmissionForm(request.POST or None, request.FILES)
    else:
        # get current submission, pass it as an instance if it exists
        current_submission = TextSubmission.objects.filter(assignment=assignment).filter(student=request.user).first()
        if current_submission:
            form = TextSubmissionForm(request.POST or None, instance=current_submission)
        else:
            form = TextSubmissionForm(request.POST or None)

    # save form if it is valid
    if form.is_valid():
        submission = form.save(commit=False)
        submission.assignment = assignment
        submission.student = request.user
        submission.save()
        return redirect('course_management:coursePage', course_id)

    return render(request, 'course_management/assignment_submission.html',
                  {'course': course, 'assignment': assignment, 'path_title': str(assignment), 'form': form})

def submission_list(req, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    course = assignment.course
    submissions = Submission.objects.filter(assignment=assignment)
    grade_distrib_dataset = build_submission_data(submissions)

    ctx = {
        'assignment': assignment,
        'course': course,
        'submissions': submissions
    }
    # Don't generate graphs unless there's 2 or more graded submissions
    if len(grade_distrib_dataset['grade_distrib']) > 2:
        ctx['grade_distrib_data'] = grade_distrib_dataset['grade_distrib']
        ctx['high'] = grade_distrib_dataset['high']
        ctx['low'] = grade_distrib_dataset['low']
        ctx['mean'] = grade_distrib_dataset['mean']
        
    return render(req, 'course_management/submission_list.html', ctx)

'''!
    @brief Takes the list of submissions and constructs a dataset for the grade distribution of that assignment.
    @details Gets the data set, the high, the low, the mean, and the median for the assignment.
    @return A dictionary with the grade distribution points (list) and the high, low, and mean (integer/double).
'''
def build_submission_data(submissions):
    dataset = {'grade_distrib': [['Student', 'Grade']],
               'high':   0,
               'low' :   9999,
               'mean':   0}
    
    num_submissions = 0
    working_avg = 0.0
    for submission in submissions:
        if submission.score is not None:
            # Build datapoints for graph
            data_point = [f"{submission.student.first_name} {submission.student.last_name}",
                          submission.score]
            dataset['grade_distrib'].append(data_point)
            
            # Check for high & low
            if submission.score > dataset['high']:
                dataset['high'] = submission.score
            if submission.score < dataset['low']:
                dataset['low'] = submission.score
            
            # Keep calculating mean
            num_submissions += 1
            working_avg += submission.score
            
        if num_submissions != 0:
            dataset['mean'] = round(((working_avg) / num_submissions), 1)
            
    return dataset