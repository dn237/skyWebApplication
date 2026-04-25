from django.conf import settings
from django.db import models


class Team(models.Model):
    team_id = models.AutoField(primary_key=True, db_column="id")
    team_name = models.CharField(max_length=100, default="", db_column="name")

    mission_statement = models.TextField(blank=True, default="")
    workstream_mf = models.TextField(blank=True, default="")
    focus_areas = models.TextField(blank=True, default="")
    skills_technologies = models.TextField(blank=True, default="")
    slack_channels = models.TextField(blank=True, default="")
    standup_details = models.TextField(blank=True, default="")
    agile_practices = models.TextField(blank=True, default="")

    team_wiki = models.URLField(blank=True, default="")
    github_url = models.URLField(blank=True, default="")
    jira_board_link = models.URLField(blank=True, default="")

    status = models.CharField(max_length=50, blank=True, default="")

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

    def __str__(self):
        return self.team_name

class TeamDependency(models.Model):
    source_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='downstream_dependencies'
    )

    target_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='upstream_dependencies'
    )

    dependency_type = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"{self.source_team} → {self.target_team} ({self.dependency_type})"


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=50, blank=True)

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='projects',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class Engineer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    
    # Link to Team
    team = models.ForeignKey(
        'teams.Team', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='engineers'
    )
    
    #Link to a User if they ever create an account
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='engineer_profile'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

