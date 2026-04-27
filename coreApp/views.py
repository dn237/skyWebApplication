from django.shortcuts import render

from accounts.models import UserProfile
from teams.models import Engineer, Team
from django.contrib.auth.models import User
# ================================================
# Samia
from datetime import date
from scheduler.models import Schedule


# ================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# ----->
def dashboard(request):
    # 1. Get the profile for the logged-in user
    # We use 'profile' because that is your related_name in the model
    user_profile = getattr(request.user, 'profile', None)
    
    user_team = None
    team_members = []

    if user_profile and user_profile.team:
        user_team = user_profile.team
        # 2. Get all other UserProfiles that point to the SAME team
        # This is how we get the exact teammates
        team_members = UserProfile.objects.filter(team=user_team).exclude(user=request.user)
    else:
        # Fallback if no profile/team exists yet
        team_members = UserProfile.objects.all()[:5]

    recent_teams = Team.objects.all().order_by('-team_id')

    # Samia  - Dashboard mini calendar
    today = date.today()
    upcoming_schedules = Schedule.objects.filter(date__gte=today).order_by('date', 'time')[:4]

    return render(request, 'dashboard.html', {
        'my_team': user_team,
        'team_members': team_members, # These are now UserProfile objects
        'recent_teams': recent_teams,
    
    # Samia - Dashboard mini calendar
        'today': today,
        'upcoming_schedules': upcoming_schedules,
    })


# ========END OF AUTHOR'S WORK========
