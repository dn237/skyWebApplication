"""Sync team leads to profile rows.

This command makes sure every team lead has a matching UserProfile with
the right team set. It is safe to run more than once.
"""

from django.core.management.base import BaseCommand

from teams.models import Team
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Make sure each team lead has a matching UserProfile.'

    def handle(self, *args, **options):
        updated = 0
        created = 0
        for team in Team.objects.select_related('lead_user').all():
            lead = team.lead_user
            if not lead:
                continue

            # Create the profile if it is missing.
            profile, was_created = UserProfile.objects.get_or_create(user=lead)
            if was_created:
                created += 1

            # Keep the profile tied to the team the user leads.
            if profile.team_id != team.pk:
                profile.team = team
                profile.save(update_fields=['team'])
                updated += 1

        self.stdout.write(f'Created profiles: {created}, Updated team links: {updated}')
