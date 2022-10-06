from . import views
from django.urls import path
from django.contrib.auth import views as authentication_views

# Namespacing!
app_name = 'course_management'

urlpatterns = [
    path('', views.course_management, name='coursesMain'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('<int:id>', views.coursePage, name='coursePage'),
    path('updateCourse/<int:id>', views.updateCourse, name="updateCourse"),
    path('deleteCourse/<int:id>', views.deleteCourse, name="deleteCourse"),
    path('registration/', views.studentCourses, name='studentCourses'),
    path('registration/register/<int:id>', views.register, name='register'),
    path('registration/drop/<int:id>', views.drop, name='drop'),
    path('<int:id>/addAssignment', views.addAssignment, name='addAssignment'),
]
