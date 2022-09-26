from . import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
]