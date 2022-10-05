from . import views
from django.urls import path
from django.contrib.auth import views as authentication_views

# Namespacing!
app_name = 'course_management'

urlpatterns = [
    path('', views.course_management, name='coursesMain'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('<int:id>', views.coursePage, name='coursePage'),
    path('<int:id>/updateCourse', views.updateCourse, name="updateCourse"),
    path('<int:id>/deleteCourse', views.deleteCourse, name="deleteCourse"),
    path('<int:id>/addAssignment', views.addAssignment, name='addAssignment'),
]
