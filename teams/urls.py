from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    # The main list of all teams
    path('', views.teamsHome, name='index'), 
    # Specific team profile
    path('<int:team_id>/', views.teamsProfile, name='detail'),    
]