from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from teams.models import Team

class Command(BaseCommand):
    help = 'Master command to seed data and repair team/profile links.'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- Starting Master Sync & Seed ---")
        
        updated = 0
        created = 0
        
        # select_related fetches the User and Team in one go to save memory
        teams = Team.objects.select_related('lead_user').all()
        
        for team in teams:
            lead = team.lead_user
            if not lead:
                continue

            # 1. Repair missing profiles
            profile, was_created = UserProfile.objects.get_or_create(user=lead)
            if was_created:
                created += 1

            # 2. Repair Team Mismatches (The Alexander Perry Fix)
            # Use _id to compare the database integers directly
            if profile.team_id != team.pk: # type: ignore
                profile.team = team
                
                # OPTIONAL: If their job_title was wrong, we can fix it here too
                if profile.job_title != "Team Lead":
                     profile.job_title = "Team Lead"
                
                profile.save() 
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Final Stats -> Created: {created} | Repaired Links: {updated}'
        ))
        self.stdout.write("--- System is now Synchronized ---")