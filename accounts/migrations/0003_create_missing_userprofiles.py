"""
Data migration: create missing UserProfile rows

This migration iterates all existing `User` records and ensures a
corresponding `accounts.UserProfile` exists. It is intended to make the
transition from legacy person records to a single profile table safe by
provisioning profiles for users that don't yet have them.

The reverse operation is intentionally a no-op to avoid accidental data
removal on rollback.
"""

from django.conf import settings
from django.db import migrations


def forwards_create_profiles(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    UserProfile = apps.get_model('accounts', 'UserProfile')

    for user in User.objects.all():
        # create if missing; keep defaults for job_title/avatar
        UserProfile.objects.get_or_create(user=user)


def backwards_noop(apps, schema_editor):
    # Do not delete profiles on rollback to avoid losing data.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_avatar_userprofile_job_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(forwards_create_profiles, backwards_noop),
    ]
