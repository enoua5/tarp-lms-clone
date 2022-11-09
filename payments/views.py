from django.shortcuts import render
from course_management.models import Course
from django.contrib.auth.models import Group
from .models import Tuition

# Create your views here.
def tuition(request):
    # A precaution, in case student/course relationship does not exist
    try:        
        course_list = request.user.courses.all()
        balance = float(Tuition.objects.get(user=request.user).balance)
        total = getSemesterTotal(request.user)
        amt_paid = total - balance

        return render(request, 'payments/tuition_page.html', {'course_list': course_list,
                                                              'balance': f"{balance:0.2f}",
                                                              'total': f"{total:0.2f}",
                                                              'paid': f"{amt_paid:0.2f}"})
    except:  
        return render(request, 'payments/tuition_page.html', {'course_list' : {}})


## Supporting Functions
'''!
    @brief Calculates the total cost of the semester for the student.
    @param student The student object.
    @return total The total cost of the semester for the student (before payment).
'''
def getSemesterTotal(student):
    course_list = student.courses.all()
    total = 0.0
    
    for course in course_list:
        total += course.credit_hours * 100.0
        
    return total