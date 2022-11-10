from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Course, Assignment, Submission, FileSubmission, TextSubmission
from payments.models import Tuition
from course_management.forms import CourseForm, AssignmentForm, FileSubmissionForm, TextSubmissionForm, GradeSubmissionForm

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

    assignments = Assignment.objects.filter(course=course).order_by('due_date')
    late_list = []
    upcoming_list = []
    submitted_list = []
    for assignment in assignments:
        assignment_meta = {}
        try:
            submission = Submission.objects.get(assignment=assignment, student=request.user)
        except(Submission.DoesNotExist):
            submission = None
        submitted = submission != None
        assignment_meta['submitted'] = submitted
        if submitted:
            assignment_meta['score'] = submission.score
        else:
            if assignment.overdue():
                assignment_meta['late'] = True

        assignment_obj = {'info': assignment, 'meta': assignment_meta}
        if assignment_meta.get('late'):
            late_list.append(assignment_obj)
        elif assignment_meta.get('submitted'):
            submitted_list.append(assignment_obj)
        else:
            upcoming_list.append(assignment_obj)

    # Only calculate grade if user is a student
    if request.user.groups.filter(name='Student').exists():
        grade_list = []
        grade = course.getStudentGrade(request.user)
        for student in course.students.all():
            student_grade = course.getStudentGrade(student)
            if student_grade['percent'] >= 0.0:
                grade_list.append(student_grade['percent'])

        return render(request, 'course_management/course_page.html', {'course': course, 'page_title': str(course),
                                                                        'assignment_list': late_list + upcoming_list + submitted_list,
                                                                        'letterGrade': grade['letter'],
                                                                        'percentGrade': (str(grade['percent']) if grade['percent'] >=0 else '--'),
                                                                        'grade_list': grade_list})

    return render(request, 'course_management/course_page.html', {'course': course, 'page_title': str(course),
                                                                  'assignment_list': late_list + upcoming_list + submitted_list})

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

# Student Assignment View
def assignmentView(request, course_id, assignment_id):
    # Get assignment and check if the student has already submitted something.
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    context = {'course': course,
               'assignment' : assignment}
    # Add grade information to context here.
    student_grade = course.getStudentGrade(request.user)
    context['percentGrade'] = str(student_grade['percent']) if student_grade['percent'] >=0 else '--'
    context['letterGrade'] = student_grade['letter']
    
    if assignment.type == 'f':
        submission = FileSubmission.objects.filter(assignment=assignment).filter(student=request.user).first()
        if submission:
            context['type'] = 'file'
    else:
        submission = TextSubmission.objects.filter(assignment=assignment).filter(student=request.user).first()
        if submission:
            context['type'] = 'text'
        
    if submission:
        context['submission'] = submission
        classGrades = list(map(lambda x:x.score, getGradedSubmissions(assignment)))
        if len(classGrades) >= 2:
            context['grade_list'] = classGrades
        
    return render(request=request,
                  template_name='course_management/assignment_view.html',
                  context=context) 
        


# assignment submission view - distinguishes between file and text submission
def assignmentSubmission(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id)
    context = {}

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

    # Add grade information to context here.
    student_grade = course.getStudentGrade(request.user)
    context['percentGrade'] = str(student_grade['percent']) if student_grade['percent'] >=0 else '--'
    context['letterGrade'] = student_grade['letter']
    
    # Add other items here
    context['course'] = course
    context['assignment'] = assignment
    context['path_title'] = str(assignment)
    context['form'] = form
    
    return render(request, 'course_management/assignment_submission.html', context)

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
    if len(grade_distrib_dataset['grade_distrib']) > 3:
        ctx['grade_distrib_data'] = grade_distrib_dataset['grade_distrib']
        ctx['high'] = grade_distrib_dataset['high']
        ctx['low'] = grade_distrib_dataset['low']
        ctx['mean'] = grade_distrib_dataset['mean']
        ctx['danger_students'] = get_danger_students(assignment)
        ctx['succeeding_students'] = get_succeeding_students(assignment)

    return render(req, 'course_management/submission_list.html', ctx)


def gradeSubmission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)

    if submission.assignment.type == 'f':
        submission = FileSubmission.objects.get(id=submission_id)
    else:
        submission = TextSubmission.objects.get(id=submission_id)

    course = submission.assignment.course

    form = GradeSubmissionForm(request.POST or None, instance=submission)
    if form.is_valid():
        form.save()
        return redirect('course_management:submission_list', submission.assignment.id)

    return render(request, 'course_management/grade_submission.html', {'course': course, 'submission': submission, 'form': form})


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


'''!
    @brief Gets a list of the given assignment's graded submissions.
    @param assignment The assignment object.
    @return A list of submission objects for that assignment.
'''
def getGradedSubmissions(assignment):
    allSubmissions = Submission.objects.filter(assignment=assignment)
    gradedSubmissions = filter(lambda grade: grade is not None, allSubmissions)
    return gradedSubmissions

'''!
    @brief Takes an assignment, grabs all graded submissions for the assignment, and returns a list of students in the "danger zone"
    @details Students with grades in the bottom 20% of possible points for this assignment are in the danger zone
    @return A list of student objects in the "danger zone" for the associated assignment
'''
def get_danger_students(assignment):
    submissions = Submission.objects.filter(assignment=assignment)
    danger_students = []

    if submissions:
        for submission in submissions:
            if submission.score and submission.score < (assignment.points * 0.2):
                danger_students.append(submission.student)

    return danger_students


'''!
    @brief Takes an assignment, grabs all graded submissions for the assignment, and returns a list of students in the "high score zone"
    @details Students with grades in the top 20% of possible points for this assignment are in the high score zone
    @return A list of student objects in the "high score zone" for the associated assignment
'''
def get_succeeding_students(assignment):
    submissions = Submission.objects.filter(assignment=assignment)
    succeeding_students = []

    if submissions:
        for submission in submissions:
            if submission.score and submission.score > (assignment.points * 0.8):
                succeeding_students.append(submission.student)

    return succeeding_students
