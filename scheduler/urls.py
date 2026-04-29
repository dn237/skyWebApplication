# AUTHOR: SAMIA EL HAYARI RIFI | STUDENT ID: 20899864
# Scheduler views (create, list, edit, delete)

from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('create/', views.create_schedule, name='create_schedule'),
    path('tasks/', views.task_list, name='task_list'),
    path('edit/<int:id>/', views.edit_schedule, name='edit_schedule'),
    path('delete/<int:id>/', views.delete_schedule, name='delete_schedule'),
]
