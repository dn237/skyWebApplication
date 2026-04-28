# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.contrib import admin
from .models import Team, Project, TeamDependency
from .models import TeamUpdate

# Admin setup for Team, Project, and TeamDependency.
# People data now lives in accounts.UserProfile, so there is no separate
# Engineer admin anymore.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin view for teams."""
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

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin view for projects."""
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

@admin.register(TeamDependency)
class TeamDependencyAdmin(admin.ModelAdmin):
    """Admin view for team links."""
    list_display = ("source_team", "target_team", "dependency_type")
    search_fields = ("source_team__team_name", "target_team__team_name")


@admin.register(TeamUpdate)
class TeamUpdateAdmin(admin.ModelAdmin):
    list_display = ('team', 'title', 'author', 'created_at')
    list_filter = ('team', 'created_at')
    search_fields = ('title', 'body')
