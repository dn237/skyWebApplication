"""
Management command: sync_team_profiles

This command ensures that each Team.lead_user has a corresponding
`accounts.UserProfile` with the `team` field set to the team they lead.

Reason: we migrated away from the legacy `Engineer` model and now keep
team membership on the UserProfile. Some legacy data imports or edge
cases may have left lead users without a linked profile — this command
fixes that in bulk.

Run: `python manage.py sync_team_profiles`

This command is idempotent and safe to re-run.
"""

from django.core.management.base import BaseCommand

from teams.models import Team
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Ensure Team.lead_user has a UserProfile.team set to the team they lead.'

    def handle(self, *args, **options):
        updated = 0
        created = 0
        for team in Team.objects.select_related('lead_user').all():
            lead = team.lead_user
            if not lead:
                continue

            # get_or_create ensures the user has a profile; was_created
            # tells us whether we made a new profile for a user that
            # previously didn't have one.
            profile, was_created = UserProfile.objects.get_or_create(user=lead)
            if was_created:
                created += 1

            # Use .pk for portability in case the Team model uses a
            # non-standard primary key name.
            if profile.team_id != team.pk:
                profile.team = team
                profile.save(update_fields=['team'])
                updated += 1

        self.stdout.write(f'Created profiles: {created}, Updated team links: {updated}')
