

from django.shortcuts import get_object_or_404, render

from .models import Team


def teamsHome(request):
    teams = Team.objects.all()
    departments = (
        Team.objects.select_related("dept")
        .values_list("dept__dept_name", flat=True)
        .order_by("dept__dept_name")
        .distinct()
    )

    return render(request, "teams/team_list.html", {
        "teams": teams,
        "departments": departments,
    })

def teamsProfile(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, 'teams/team_profile.html', {'team': team})