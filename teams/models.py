gitfrom django.conf import settings
from django.db import models


from django.db import models
from django.conf import settings

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


        class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    def __str__(self):
        return self.name