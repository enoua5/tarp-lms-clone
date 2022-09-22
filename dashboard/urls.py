from django.urls import path
import dashboard.views as dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard, name="Dashboard")
]