from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Coauthor: Anita  | STUDENT ID:
# =================================================

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

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