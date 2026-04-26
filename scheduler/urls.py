from django.urls import path
from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('create/', views.create_schedule, name='create_schedule'),
    path('edit/<int:id>/', views.edit_schedule, name='edit_schedule'),
    path('delete/<int:id>/', views.delete_schedule, name='delete_schedule'),
]