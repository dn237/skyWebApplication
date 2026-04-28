import os
import sys
import django

# Ensure the project root is on sys.path so imports like `coreApp.settings`
# resolve when this script is executed directly.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Ensure settings are loaded from the project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coreApp.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from teams.models import Team

User = get_user_model()

u = User.objects.filter(pk=2).first()
print('USER:', repr(u), 'id:', getattr(u, 'id', None))

p = UserProfile.objects.filter(user_id=2).first()
print('PROFILE:', p)
print('PROFILE.team_id:', getattr(p, 'team_id', None))

t = Team.objects.filter(lead_user_id=2).first()
print('TEAM where lead_user=2:', t)
if t:
    print('Team.pk:', t.pk)
    members = list(
        UserProfile.objects.filter(team=t).values_list('user__id', 'user__username', 'job_title')
    )
    print('Profiles in that team:', members)
else:
    print('No team found with lead_user=2')
