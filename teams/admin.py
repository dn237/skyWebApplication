from django.contrib import admin
from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'team_name',
        'dept',
        'project',
        'lead_user',
        'status',
    )

    list_filter = (
        'dept',
        'project',
        'status',
    )

    search_fields = (
        'team_name',
        'mission_statement',
        'focus_areas',
    )

    fieldsets = (
        ("Basic Info", {
            'fields': ('team_name', 'dept', 'project', 'lead_user', 'status')
        }),

        ("Team Details", {
            'fields': (
                'mission_statement',
                'workstream_mf',
                'focus_areas',
                'skills_technologies',
            )
        }),

        ("Tools & Resources", {
            'fields': (
                'github_url',
                'jira_board_link',
                'software_owned',
                'team_wiki',
            )
        }),

        ("Communication & Process", {
            'fields': (
                'slack_channels',
                'standup_details',
                'agile_practices',
            )
        }),
    )
    
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'jira_name',
        'status',
        'start_date',
        'end_date',
    )

    list_filter = (
        'status',
        'start_date',
    )

    search_fields = (
        'name',
        'jira_name',
        'description',
        'objectives',
    )

    
    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'jira_name', 'status')
        }),

        ("Project Details", {
            'fields': ('description', 'objectives')
        }),

        ("Timeline", {
            'fields': ('start_date', 'end_date')
        }),
    )
    

    from .models import TeamDependency

    @admin.register(TeamDependency)
    class TeamDependencyAdmin(admin.ModelAdmin):
    list_display = ("source_team", "target_team", "dependency_type")
    search_fields = ("source_team__team_name", "target_team__team_name")