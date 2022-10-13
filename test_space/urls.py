from django.urls import path
from . import views

# App Name
app_name = 'test'
urlpatterns = [
    path('', views.index, name="index"),
    path('template', views.template, name="Template Loading"),
    path('accountype', views.accounttype, name="Account Type"),
    path('stats', views.stats, name="Stats"),
    path('rest/', views.rest_api, name="Rest API Test")
]