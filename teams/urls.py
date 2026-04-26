from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    # The main list of all teams
    path('', views.teamsHome, name='index'), 
    # Specific team profile
    path('teamID-<int:team_id>/profile', views.teamsProfile, name='detail'),    
    # Team members page 
    path('teamID-<int:team_id>/members/', views.teamMembers, name='members'),
    # Team projects page
    path('teamID-<int:team_id>/projects/', views.teamProjects, name='projects'),
    # Team dependencies page
    path('teamID-<int:team_id>/dependencies/', views.teamDependencies, name='dependencies'),
    # Repositories page
    path('teamID-<int:team_id>/repositories/', views.teamRepositories, name='repositories'),
]