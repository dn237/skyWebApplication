from django.urls import path
from . import views

# Setting the app namespace to avoid URL name collisions
app_name = 'organizations'

urlpatterns = [
    # Mapping the root URL of this app to the organization_list view
    # Example: http://127.0.0.1:8000/organizations/
    path('', views.organization_list, name='dept'),
]