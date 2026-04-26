from django.urls import path
from . import views

# Application namespace for reverse URL lookups
app_name = 'organizations'

urlpatterns = [
    # Main list page: /organizations/
    # Name 'dept' matches Diana's link in base.html
    path('', views.organization_list, name='dept'),
    
    # Detail page: /organizations/1/ or /organizations/2/
    # <int:pk> is a path converter that captures the ID from the URL
    path('<int:pk>/', views.department_detail, name='detail'),
    path('add/', views.create_department, name='add_department'),
    path('<int:pk>/edit/', views.edit_department, name='edit_department'),
    path('<int:pk>/delete/', views.delete_department, name='delete_department'),
]