from django.urls import path
from . import views

urlpatterns = [
    path('', views.teamsHome, name='teamsHome'),
    path('<int:team_id>/', views.teamDetail, name='teamDetail'),    
]