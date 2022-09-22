from django.urls import path
import dashboard.views as dashboard_views

# App Name
app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_views.dashboard, name="dashboard")
]