# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.contrib import admin
from .models import Team, Project, TeamDependency


# --- 1. Team Administration ---
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Main Team configuration. 
    Organizes team metadata, tools, and processes into logical fieldsets.
    """
    list_display = ('team_name', 'dept', 'lead_user', 'status')
    list_filter = ('dept', 'status')
    search_fields = ('team_name', 'mission_statement', 'focus_areas')

    fieldsets = (
        ("Basic Identification", {
            'fields': ('team_name', 'dept', 'lead_user', 'status')
        }),
        ("Strategic Details", {
            'fields': ('mission_statement', 'workstream_mf', 'focus_areas', 'skills_technologies')
        }),
        ("External Integration", {
            'fields': ('github_url', 'jira_board_link', 'team_wiki')
        }),
        ("Operational Workflow", {
            'fields': ('slack_channels', 'standup_details', 'agile_practices')
        }),
    )

# --- 2. Project Administration ---
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Tracking for specific initiatives assigned to Teams.
    """
    list_display = ('name', 'status', 'team', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'team')
    search_fields = ('name', 'description')
    
    fieldsets = (
        ("General Info", {
            'fields': ('name', 'status', 'team')
        }),
        ("Description", {
            'fields': ('description',)
        }),
        ("Timeline", {
            'fields': ('start_date', 'end_date')
        }),
    )

# --- 3. Dependency Mapping ---
@admin.register(TeamDependency)
class TeamDependencyAdmin(admin.ModelAdmin):
    """
    Visualizes the connections and blockers between different squads.
    """
    list_display = ("source_team", "target_team", "dependency_type")
    search_fields = ("source_team__team_name", "target_team__team_name")
