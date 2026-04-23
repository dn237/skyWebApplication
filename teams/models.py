from django.conf import settings
from django.db import models


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)

    team_name = models.CharField(max_length=100)

    mission_statement = models.TextField(blank=True)
    workstream_mf = models.TextField(blank=True)
    focus_areas = models.TextField(blank=True)
    skills_technologies = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    jira_board_link = models.URLField(blank=True)
    software_owned = models.TextField(blank=True)
    slack_channels = models.TextField(blank=True)
    standup_details = models.TextField(blank=True)
    agile_practices = models.TextField(blank=True)
    team_wiki = models.URLField(blank=True)
    status = models.CharField(max_length=50, blank=True)

    dept = models.ForeignKey(
        "organizations.Department",
        on_delete=models.PROTECT,
        related_name="teams",
        null=True,
        blank=True,
    )

    lead_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="led_teams",
        null=True,
        blank=True,
    )

    project = models.ForeignKey(
        "teams.Project",
        on_delete=models.SET_NULL,
        related_name="teams",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.team_name



class Project(models.Model):
    project_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)
    objectives = models.TextField(blank=True)

    jira_name = models.CharField(max_length=200)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True
    )

    def __str__(self):
        return self.name