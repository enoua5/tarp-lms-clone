from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('', views.tuition, name='tuition'),
    path("create-payment-intent/", views.createpayment, name="create-payment-intent"),
    path('success/', views.success, name='success')
]