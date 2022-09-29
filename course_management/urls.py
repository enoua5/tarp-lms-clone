from . import views
from django.urls import path
from django.contrib.auth import views as authentication_views

# Namespacing!
app_name = 'course_management'

urlpatterns = [
    path('', views.course_management, name='coursesMain'),
    path('addCourse/', views.addCourse, name='addCourse'),
    #path('updateCourse/<int:id>', views.updateCourse, name="update"),
    #path('deleteCourse/<int:id>', views.deleteCourse, name="delete"),
]
