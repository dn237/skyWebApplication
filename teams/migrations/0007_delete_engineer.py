import re

from django.conf import settings
from django.db import migrations
from django.contrib.auth.hashers import make_password


def forwards_transfer_engineers(apps, schema_editor):
    Engineer = apps.get_model("teams", "Engineer")
    UserProfile = apps.get_model("accounts", "UserProfile")
    user_app_label, user_model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(user_app_label, user_model_name)

    for engineer in Engineer.objects.select_related("user", "team").all():
        user = engineer.user

        if user is None:
            base_source = engineer.email or f"{engineer.first_name}.{engineer.last_name}" or "engineer"
            base_username = re.sub(r"[^a-zA-Z0-9_.-]+", "", base_source).strip("._-").lower() or "engineer"
            username = base_username
            suffix = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{suffix}"
                suffix += 1

            user = User.objects.create(
                username=username,
                first_name=engineer.first_name,
                last_name=engineer.last_name,
                email=engineer.email or "",
                password=make_password(None),
            )

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "team": engineer.team,
                "job_title": "Engineer",
            },
        )


def backwards_transfer_engineers(apps, schema_editor):
    UserProfile = apps.get_model("accounts", "UserProfile")
    Engineer = apps.get_model("teams", "Engineer")

    for profile in UserProfile.objects.select_related("user", "team").filter(job_title="Engineer"):
        if profile.user_id is None:
            continue

        Engineer.objects.get_or_create(
            user=profile.user,
            defaults={
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "email": profile.user.email,
                "team": profile.team,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile_avatar_userprofile_job_title_and_more"),
        ("teams", "0006_alter_team_github_url_alter_team_jira_board_link"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            forwards_transfer_engineers,
            backwards_transfer_engineers,
        ),
    ]