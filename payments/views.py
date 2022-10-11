from django.shortcuts import render
from course_management.models import Course

# A helper function to calculate the balance of a student
def calculateBalance(course_list):
    # Total credit hours
    chrs = 0

    # Adds all credit hours together 
    for course in course_list:
        chrs += course.credit_hours

    return chrs*100

# Create your views here.
def tuition(request):
    # A precaution, in case student/course relationship does not exist
    try:        
        course_list = request.user.courses.all()
        balance = calculateBalance(course_list)
        return render(request, 'payments/tuition_page.html', {'course_list' : course_list, 'balance' : balance})
    except:  
        return render(request, 'payments/tuition_page.html', {'course_list' : {}})

