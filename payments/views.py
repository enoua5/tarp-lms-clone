from django.shortcuts import render, redirect
from course_management.models import Course
from django.contrib.auth.models import Group
from .models import Tuition
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings 
import json
from django.http import JsonResponse

# A landing page for tuition
def tuition(request):
    # A precaution, in case student/course relationship does not exist
    try:        
        course_list = request.user.courses.all()
        balance = float(Tuition.objects.get(user=request.user).balance)
        total = getSemesterTotal(request.user)
        amt_paid = total - balance

        return render(request, 'payments/tuition_page.html', {'course_list': course_list,
                                                              'balance': balance,
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
  
# Stripe nonsence 
@csrf_exempt
def createpayment(request):
  if request.user.is_authenticated:
    balance = Tuition.objects.get(user=request.user).balance * 100

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method=="POST":
      data = json.loads(request.body)
      # Create a PaymentIntent with the order amount and currency
      intent = stripe.PaymentIntent.create(
        amount=int(balance),
        payment_method_types=['card'],
        currency=data['currency'],
        metadata={'integration_check': 'accept_a_payment'},
        )
      # print(intent.client_secret)
      try:
        return JsonResponse({'publishableKey':  
          settings.STRIPE_PUBLIC_KEY, 'clientSecret': intent.client_secret})
      except Exception as e:
        return JsonResponse({'error':str(e)},status= 403)


def success(request):
    # Alright. I am not going to check if transaction was successful
    # Just trusting that it is
    currTuition = Tuition.objects.get(user=request.user)

    # Variables needed for receipt
    paid = currTuition.balance

    currTuition.balance = 0
    currTuition.save()

    course_list = request.user.courses.all()
    balance = float(Tuition.objects.get(user=request.user).balance)
    total = getSemesterTotal(request.user)

    return render(request, 'payments/tuition_page.html', {'course_list' : course_list,
                                                          'balance' : balance,
                                                          'total': total,
                                                          'paid': paid,
                                                          'success' : True}) 
