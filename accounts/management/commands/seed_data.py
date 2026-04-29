# ================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Master Sync & Excel Data Ingestion
# ================================================

import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from teams.models import Team, TeamDependency, Project
from organizations.models import Department

class Command(BaseCommand):
    help = 'Master command to import Excel data and repair team/profile links.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("--- PHASE 1: EXCEL INGESTION ---"))
        
        try:
            df = pd.read_excel("Agile Project Module UofW - Team Registry.xlsx")
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Excel file not found in project root!"))
            return

        # 1. Departments + Teams + Team Leads
        for _, row in df.iterrows():
            dept_name = str(row.get("Department", "")).strip()
            team_name = str(row.get("Team Name", "")).strip()
            head_name = str(row.get("Department Head", "")).strip()
            lead_name = str(row.get("Team Leader", "")).strip()

            if not team_name or team_name == "nan":
                continue

            # --- Handle Dept Head (User) ---
            manager = None
            if head_name and head_name != "nan":
                username = head_name.replace(" ", "").lower()
                manager, _ = User.objects.get_or_create(
                    username=username,
                    defaults={"first_name": head_name}
                )

            # --- Handle Team Leader (User) ---
            lead_user = None
            if lead_name and lead_name != "nan":
                username = lead_name.replace(" ", "").lower()
                lead_user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={"first_name": lead_name}
                )

            # --- Create Department ---
            dept, _ = Department.objects.get_or_create(
                dept_name=dept_name,
                defaults={"head_user": manager}
            )

            # --- Create Team ---
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
                    "status": "Active"
                }
            )

            # --- Ensure Team Lead UserProfile exists ---
            if lead_user:
                profile, _ = UserProfile.objects.update_or_create(
                    user=lead_user,
                    defaults={
                        "team": team,
                        "job_title": "Team Lead",
                    },
                )
                profile.save() # Triggers signals

        # 2. Projects
        for _, row in df.iterrows():
            team_name = str(row.get("Team Name", "")).strip()
            project_name = str(row.get("Jira Project Name", "")).strip()
            if not project_name or project_name == "nan": continue

            try:
                team = Team.objects.get(team_name=team_name)
                description = f"{row.get('Project (codebase) (Github Repo)', '')} | {row.get('Software Owned', '')}"
                Project.objects.get_or_create(name=project_name, team=team, defaults={"description": description})
            except Team.DoesNotExist:
                continue

        # 3. Dependencies
        for _, row in df.iterrows():
            team_name = str(row.get("Team Name", "")).strip()
            downstream = str(row.get("Downstream Dependencies", "")).strip()
            if not team_name or not downstream or downstream == "nan": continue

            try:
                source_team = Team.objects.get(team_name=team_name)
                for dep in downstream.split(","):
                    target_team = Team.objects.get(team_name=dep.strip())
                    TeamDependency.objects.get_or_create(source_team=source_team, target_team=target_team)
            except Team.DoesNotExist:
                continue

        self.stdout.write(self.style.NOTICE("--- PHASE 2: SYSTEM REPAIR & SYNC ---"))
        
        repaired = 0
        teams = Team.objects.select_related('lead_user').all()
        
        for team in teams:
            lead = team.lead_user
            if not lead: continue

            profile, _ = UserProfile.objects.get_or_create(user=lead)
            
            # Reconciliation Logic: If profile data doesn't match Team model data
            if profile.team != team.pk or profile.job_title != "Team Lead":
                profile.team = team
                profile.job_title = "Team Lead"
                profile.save() # Re-verify via Signal
                repaired += 1

        self.stdout.write(self.style.SUCCESS(f"Master Sync Complete. Repaired {repaired} profiles."))