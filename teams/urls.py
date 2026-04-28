# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

"""Routes for the teams app."""

from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    # Main teams page
    path('', views.TeamListView.as_view(), name='index'), 
    # Team profile page
    path('teamID-<int:team_id>/profile', views.TeamDetailView.as_view(), name='detail'),    
    # Team members page
    path('teamID-<int:team_id>/members/', views.teamMembers, name='members'),
    # Team projects page
    path('teamID-<int:team_id>/projects/', views.teamProjects, name='projects'),
    # Team dependencies page
    path('teamID-<int:team_id>/dependencies/', views.teamDependencies, name='dependencies'),
    # Repositories page
    path('teamID-<int:team_id>/repositories/', views.teamRepositories, name='repositories'),
    # Edit team page
    path('teamID-<int:team_id>/edit/', views.TeamUpdateView.as_view(), name='edit'),
    
    path('projects/<int:pk>/', views.projectDetail, name='project_detail'),
    # Update tools for team leads
    path('teamID-<int:team_id>/updates/add/', views.TeamUpdateCreateView.as_view(), name='add_update'),
    path('teamID-<int:team_id>/updates/<int:update_id>/delete/', views.TeamUpdateDeleteView.as_view(), name='delete_update'),
    path('teamID-<int:team_id>/updates/manage/', views.TeamUpdateManageView.as_view(), name='manage_updates'),
    path('teamID-<int:team_id>/updates/older/', views.older_team_updates, name='older_updates'),

]