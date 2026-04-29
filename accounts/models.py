from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  # <--- Added
from typing import TYPE_CHECKING

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Coauthor: Anita  | STUDENT ID: 2076892
# =================================================

if TYPE_CHECKING:
    from teams.models import Team
    from organizations.models import Department

class UserProfile(models.Model):
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

    @property
    def role(self):
        if not self.team:
            return self.job_title if self.job_title else "Independent Contributor"
    
        if self.team.dept and self.team.dept.head_user_id == self.user.pk:
            return "Department Head"
        if self.team.lead_user_id == self.user.pk:
            return "Team Lead"
        # 4. Fallback: If they lead ANOTHER team but not this one,
        # they show up as their standard job title (e.g., 'Senior Engineer')
        return self.job_title if self.job_title else "Team Member"

    def clean(self):
        """
        Automatic Data Verification:
        Ensures the profile department matches the team's assigned department.
        """
        if self.team and self.department:
            # We compare the actual department objects or their IDs
            if self.team.dept_id != self.department.pk:
                raise ValidationError({
                    'department': f"Data Mismatch: Team '{self.team}' belongs to '{self.team.dept}', "
                                  f"but profile tried to assign '{self.department}'."
                })

    def save(self, *args, **kwargs):
        """
        Custom save to trigger validation and sync department.
        """
        # 1. Pull the department from the team automatically if not set
        if self.team and self.team.dept:
            self.department = self.team.dept
            
        # 2. Run the clean() method checks
        self.full_clean()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"