from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def teamsPage(request):
    return HttpResponse("<h1>Teams App</h1><p>Setup Successful! Student 1, start coding here.</p>")