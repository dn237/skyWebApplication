from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Q
from .models import Team

def teamsHome(request):
    # 1. Capture View Preference (Grid vs List)
    # Default to 'grid' to match Teams1 Figma
    view_type = request.GET.get("view", "grid") 

    # 2. Existing Search/Filter/Sort Logic
    search_query = request.GET.get("q", "").strip()
    selected_departments = request.GET.getlist("departments")
    selected_sort = request.GET.get("sort", "name_asc")

    teams = Team.objects.select_related("dept", "lead_user").annotate(
        # name must match what used in HTML
        computed_count=Count("engineers", distinct=True), 
        repo_count=Count("projects", distinct=True) 
    )

    if search_query:
        teams = teams.filter(
            Q(team_name__icontains=search_query)
            | Q(mission_statement__icontains=search_query)
            | Q(dept__dept_name__icontains=search_query)
        )

    if selected_departments:
        teams = teams.filter(dept__dept_name__in=selected_departments)

    # Sorting logic
    if selected_sort == "name_desc":
        teams = teams.order_by("-team_name")
    elif selected_sort == "date_newest":
        teams = teams.order_by("-team_id")
    elif selected_sort == "date_oldest":
        teams = teams.order_by("team_id")
    else:
        teams = teams.order_by("team_name")

    # Get unique departments for the filter dropdown
    departments = (
        Team.objects.select_related("dept")
        .values_list("dept__dept_name", flat=True)
        .order_by("dept__dept_name")
        .distinct()
    )


    # 3. Add 'view_type' to the Context
    return render(request, "teams/team_list.html", {
        "teams": teams,
        "departments": departments,
        "search_query": search_query,
        "selected_departments": selected_departments,
        "selected_sort": selected_sort,
        "view_type": view_type, # <--- Tells HTML which layout to use
    })

from django.db.models import Count

def teamsProfile(request, team_id):
    team = get_object_or_404(
        Team.objects.select_related("dept", "lead_user").annotate(
            computed_member_count=Count("engineers", distinct=True),
            computed_repo_count=Count("projects", distinct=True)
        ), 
        pk=team_id
    )
    # Get dependencies for the sidebar
    dependencies = team.downstream_dependencies.all()
    
    return render(request, 'teams/team_profile.html', {
        'team': team,
        'dependencies': dependencies
    })

def teamMembers(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.engineers.select_related('user').all()
    
    return render(request, 'teams/team_members.html', {
        'team': team,
        'members': members
    })

def teamProjects(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    projects = team.projects.all()
    
    return render(request, 'teams/team_projects.html', {
        'team': team,
        'projects': projects
    })

def teamDependencies(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    dependencies = team.downstream_dependencies.select_related('target_team').all()
    
    return render(request, 'teams/team_dependencies.html', {
        'team': team,
        'dependencies': dependencies
    })

def teamRepositories(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    repositories = team.projects.filter(description__icontains="github.com").all()

    return render(request, 'teams/team_repositories.html', {
        'team': team,
        'repositories': repositories
    })