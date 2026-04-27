from django.shortcuts import render
from django.db.models import Q, Count  # <--- Added Q and Count
from accounts.models import UserProfile
from teams.models import Team
from datetime import date
from scheduler.models import Schedule

# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
def dashboard(request):
    user_profile = getattr(request.user, 'profile', None)
    
    # 1. CAPTURE THE SEARCH QUERY
    search_query = request.GET.get("q", "").strip()

    # 2. FILTER TEAMS BASED ON SEARCH
    # We use .annotate so the "Complex Table" can show counts if needed
    teams_base = Team.objects.select_related('dept', 'lead_user').annotate(
        member_count=Count('members', distinct=True)
    )

    if search_query:
        # Filter by name, mission, or department name
        recent_teams = teams_base.filter(
            Q(team_name__icontains=search_query) |
            Q(mission_statement__icontains=search_query) |
            Q(dept__dept_name__icontains=search_query)
        ).distinct()
    else:
        recent_teams = teams_base.order_by('-team_id')[:5]

    # 3. TEAM ROSTER LOGIC (Your existing work)
    user_team = None
    team_members = []

    if user_profile and user_profile.team:
        user_team = user_profile.team
        team_members = UserProfile.objects.filter(team=user_team).exclude(user=request.user)
    else:
        team_members = UserProfile.objects.all()[:5]

    # 4. ADMIN & CALENDAR (Samia's work)
    admin_teams = recent_teams[:5] if (request.user.is_staff or request.user.is_superuser) else []
    today = date.today()
    upcoming_schedules = Schedule.objects.filter(date__gte=today).order_by('date', 'time')[:4]

    return render(request, 'dashboard.html', {
        'my_team': user_team,
        'team_members': team_members,
        'recent_teams': recent_teams,
        'admin_teams': admin_teams,
        'search_query': search_query, # <--- Pass this back to keep text in the bar
        'today': today,
        'upcoming_schedules': upcoming_schedules,
    })