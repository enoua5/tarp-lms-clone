from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('', views.tuition, name='tuition'),
    path("create-payment-intent/", views.createpayment, name="create-payment-intent"),
    path("payment-complete/", views.paymentcomplete, name="payment-complete"),
    path('success/', views.success, name='success')
]