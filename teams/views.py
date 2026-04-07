from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def teamsHome(request):
    return render(request, 'teams/team_list.html')