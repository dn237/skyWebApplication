from django.shortcuts import render
from django.db.models import Q, Count  # <--- Added Q and Count
from accounts.models import UserProfile
from teams.models import Team
from datetime import date
from scheduler.models import Schedule
from teams.models import TeamUpdate

# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
def dashboard(request):
    """Render the main dashboard.

    The dashboard uses `accounts.UserProfile` as the authoritative source
    of profile information (team membership, job_title, avatar). This
    function is defensive: some User objects may not have a profile yet
    (profiles are created on first visit or via migrations), so we
    gracefully handle missing profiles to avoid errors.
    """
    # Robustly fetch the logged-in user's profile. Using getattr can raise
    # a RelatedObjectDoesNotExist for users without profiles, so handle that.
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
        except Exception:
            user_profile = None
    
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
    current_user_id = request.user.id if request.user.is_authenticated else None

    if user_profile and user_profile.team:
        user_team = user_profile.team
        # Show the full team roster, including the current user, so the
        # dashboard reads like a true team membership view rather than a
        # "everyone except me" list.
        team_members = sorted(
            UserProfile.objects.filter(team=user_team).select_related('user'),
            key=lambda member: (member.user_id != current_user_id, member.user.username.lower()),
        )
    else:
        # Do not show arbitrary users if the current user has no team.
        # An empty queryset will trigger the template's 'No teammates found' message.
        team_members = UserProfile.objects.none()

    # 4. ADMIN & CALENDAR (Samia's work)
    admin_teams = recent_teams[:5] if (request.user.is_staff or request.user.is_superuser) else []
    today = date.today()
    upcoming_schedules = Schedule.objects.filter(date__gte=today).order_by('date', 'time')[:4]
    # Team updates for the small dashboard card — keep only the two most
    # recent visible items. Older items are lazy-loaded from a JSON endpoint.
    total_team_updates = TeamUpdate.objects.filter(team=user_team).count() if user_team else 0
    team_updates = TeamUpdate.objects.filter(team=user_team)[:2] if user_team else []
    has_hidden_updates = total_team_updates > 2

    # No inline form on dashboard; team leads use the Add Update page.
    team_update_form = None

    return render(request, 'dashboard.html', {
        'my_team': user_team,
        'team_members': team_members,
        'current_user_id': current_user_id,
        'recent_teams': recent_teams,
        'admin_teams': admin_teams,
        'search_query': search_query, # <--- Pass this back to keep text in the bar
        'today': today,
        'upcoming_schedules': upcoming_schedules,
        'team_updates': team_updates,
        'has_hidden_updates': has_hidden_updates,
    })