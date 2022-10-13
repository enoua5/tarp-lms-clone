from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('', views.tuition, name='tuition'),
]