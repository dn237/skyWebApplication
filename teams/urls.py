# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

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
    # Edit team page
    path('teamID-<int:team_id>/edit/', views.editTeam, name='edit'),
    
    path('projects/<int:pk>/', views.projectDetail, name='project_detail'),
    # Team update management (lead users only)
    path('teamID-<int:team_id>/updates/add/', views.add_team_update, name='add_update'),
    path('teamID-<int:team_id>/updates/<int:update_id>/delete/', views.delete_team_update, name='delete_update'),
    path('teamID-<int:team_id>/updates/manage/', views.manage_team_updates, name='manage_updates'),
    path('teamID-<int:team_id>/updates/older/', views.older_team_updates, name='older_updates'),

]