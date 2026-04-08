from django.shortcuts import render

from .models import Team


def teamsHome(request):
    departments = (
        Team.objects.exclude(department__isnull=True)
        .exclude(department__exact="")
        .values_list("department", flat=True)
        .order_by("department")
        .distinct()
    )

    return render(request, "teams/team_list.html", {"departments": departments})

def teamDetail(request, team_id):
    return render(request, 'teams/team_detail.html', {'team_id': team_id})