from django.urls import path
from . import views

urlpatterns = [
    path('', views.teamsHome, name='teamsHome'),
    path('<int:team_id>/', views.teamsProfile, name='teamsProfile'),
    path('home/', views.teamsHome, name='teamsHome'),
]