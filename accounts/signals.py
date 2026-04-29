from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import UserProfile

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================
# This signal ensures that whenever a UserProfile is saved,
# we automatically check if their job title matches their actual role based on team leadership.
# If not, we correct it to maintain data integrity without relying on manual input.
# It also ensures that the department always matches the team’s department to prevent mismatches.
# This way, the app stays accurate and up-to-date with minimal manual maintenance!

@receiver(pre_save, sender=UserProfile)
def auto_verify_and_clean_role(sender, instance, **kwargs):
    """
    This runs AUTOMATICALLY every time a profile is saved.
    It ensures that if a user isn't the actual leader, 
    their hardcoded title is corrected.
    """
    if instance.team:
        # Check if they are the actual leader of their assigned team
        is_actual_lead = (instance.team.lead_user_id == instance.user.pk)
        
        # Check if they are the department head
        is_dept_head = (
            instance.department_id and 
            instance.department.head_user_id == instance.user.pk
        )

        # AUTOMATIC FIX: If they aren't a leader but the title says they are,
        # reset it to a standard role.
        if not is_actual_lead and not is_dept_head:
            if instance.job_title in ["Team Lead", "Department Head"]:
                instance.job_title = "Engineer" # Or whatever your default is
        
        # AUTOMATIC SYNC: Ensure department always matches the team
        if instance.team.dept_id:
            instance.department = instance.team.dept