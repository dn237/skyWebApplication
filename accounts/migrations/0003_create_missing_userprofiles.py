from django.conf import settings
from django.db import migrations


def forwards_create_profiles(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    UserProfile = apps.get_model('accounts', 'UserProfile')

    for user in User.objects.all():
        # create if missing
        UserProfile.objects.get_or_create(user=user)


def backwards_noop(apps, schema_editor):
    # Do not delete profiles on rollback
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_avatar_userprofile_job_title_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(forwards_create_profiles, backwards_noop),
    ]
