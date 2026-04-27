# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================
# Contributor: Anita B. - Added Project and TeamDependency models
# =================================================
# NOTE: This module contains the main Team/Project/Dependency models used
# across the app. Historically there was an `Engineer` model here that
# duplicated user/profile information. That model has been removed and
# its data migrated into `accounts.UserProfile`. Use `UserProfile` for
# person-level fields (team membership, avatar, job_title) and keep
# `Team`/`Project` here for team-scoped data.

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

    team_wiki = models.TextField(blank=True, default="")
    github_url = models.TextField(blank=True, default="")
    jira_board_link = models.TextField(blank=True, default="")

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


class TeamUpdate(models.Model):
    """A short update posted by a team's lead or members for the team's
    dashboard. Team leads are permitted to add and delete updates for their
    team via simple views and templates.
    """
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.team}: {self.title[:40]}"

