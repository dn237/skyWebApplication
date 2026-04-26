from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('create/', views.create_schedule, name='create_schedule'),
]