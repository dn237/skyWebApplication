from django.db import models
from django.conf import settings
from typing import TYPE_CHECKING


# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Coauthor: Anita  | STUDENT ID:
# =================================================

if TYPE_CHECKING:
    from teams.models import Team
    from organizations.models import Department


class UserProfile(models.Model):
    """Per-user additional metadata.

    Stores non-authentication attributes such as `team` membership,
    `department`, `avatar` image and `job_title`. Keep profile-level data
    here to avoid extending the primary User model directly.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )

    department = models.ForeignKey(
        'organizations.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    job_title = models.CharField(max_length=100, blank=True, default="Team Member")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.job_title})"