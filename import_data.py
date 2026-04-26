# ================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Co-author: COPILOT
# ----->

import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()

from django.contrib.auth.models import User
from teams.models import Engineer, Team, TeamDependency, Project
from organizations.models import Department

df = pd.read_excel("Agile Project Module UofW - Team Registry.xlsx")

# 1. Departments + Teams + Engineers
for _, row in df.iterrows():
    dept_name = str(row.get("Department", "")).strip()
    team_name = str(row.get("Team Name", "")).strip()
    head_name = str(row.get("Department Head", "")).strip()
    lead_name = str(row.get("Team Leader", "")).strip()

    if not team_name or team_name == "nan":
        continue

    # --- Department Head ---
    manager = None
    if head_name and head_name != "nan":
        username = head_name.replace(" ", "").lower()
        manager, _ = User.objects.get_or_create(
            username=username,
            defaults={"first_name": head_name}
        )

    # --- Team Leader ---
    lead_user = None
    if lead_name and lead_name != "nan":
        username = lead_name.replace(" ", "").lower()
        lead_user, _ = User.objects.get_or_create(
            username=username,
            defaults={"first_name": lead_name}
        )

    # --- Department ---
    dept, _ = Department.objects.get_or_create(
        dept_name=dept_name,
        defaults={"manager": manager}
    )

    # --- Team ---
    team, _ = Team.objects.get_or_create(
        team_name=team_name,
        defaults={
            "dept": dept,
            "lead_user": lead_user,
            "workstream_mf": str(row.get("Workstream (MF)", "")),
            "focus_areas": str(row.get("Development Focus Areas", "")),
            "skills_technologies": str(row.get("Key Skills & Technologies", "")),
            "slack_channels": str(row.get("Slack Channels", "")),
            "standup_details": str(row.get("Daily Standup Time and Link", "")),
            "agile_practices": str(row.get("Agile Practices", "")),
            "team_wiki": str(row.get("Team Wiki", "")),
            "status": "Active" # Установим Active, чтобы иконка в Figma была зеленой
        }
    )
    if lead_name and lead_name != "nan":
        parts = lead_name.split()
        f_name = parts[0]
        l_name = " ".join(parts[1:]) if len(parts) > 1 else "Leader"
        
        Engineer.objects.get_or_create(
            first_name=f_name,
            last_name=l_name,
            team=team
        )


# 2. Projects

for _, row in df.iterrows():
    team_name = str(row.get("Team Name", "")).strip()
    project_name = str(row.get("Jira Project Name", "")).strip()

    if not project_name:
        continue

    try:
        team = Team.objects.get(team_name=team_name)
    except Team.DoesNotExist:
        continue

    description = (
        str(row.get("Project (codebase) (Github Repo)", "")) + " | " +
        str(row.get("Software Owned and Evolved By This Team", ""))
    )

    Project.objects.get_or_create(
        name=project_name,
        team=team,
        defaults={"description": description}
    )


# 3. Dependencies

for _, row in df.iterrows():
    team_name = str(row.get("Team Name", "")).strip()
    downstream = str(row.get("Downstream Dependencies", "")).strip()
    dep_type = str(row.get("Dependency Type", "")).strip()

    if not team_name or not downstream:
        continue

    try:
        source_team = Team.objects.get(team_name=team_name)
    except Team.DoesNotExist:
        continue

    deps = downstream.split(",")

    for dep in deps:
        dep = dep.strip()
        if not dep:
            continue

        try:
            target_team = Team.objects.get(team_name=dep)
        except Team.DoesNotExist:
            continue

        TeamDependency.objects.get_or_create(
            source_team=source_team,
            target_team=target_team,
            defaults={"dependency_type": dep_type}
        )

print("IMPORT COMPLETE")

# =================================================