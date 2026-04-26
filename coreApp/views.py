from django.shortcuts import render

from teams.models import Team
from django.contrib.auth.models import User


# ================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# ----->
def dashboard(request):
    # Fetch data for your active sections
    recent_teams = Team.objects.all()
    # Assuming engineers are linked to teams
    team_members = User.objects.filter(groups__name='Engineers')
    
    return render(request, 'dashboard.html', {
        'recent_teams': recent_teams,
        'team_members': team_members,
    })

## ========END OF AUTHOR'S WORK========