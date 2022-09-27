from django.urls import path
from . import views

# App Name
app_name = 'test'
urlpatterns = [
    path('', views.index, name="index"),
    path('template', views.template, name="Template Loading"),
]