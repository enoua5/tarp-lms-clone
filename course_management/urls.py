from . import views
from django.urls import path
from django.contrib.auth import views as authentication_views

# Namespacing!
app_name = 'course_management'

urlpatterns = [
    path('', views.course_management, name='courses'),
    #path('add/', views.addUser, name='addUser'),
    #path('update/<int:id>', views.updateUser, name="update"),
    #path('delete/<int:id>', views.deleteUser, name="delete"),
]
