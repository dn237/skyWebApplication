"""
File: site_settings/urls.py
Author: Yusuf (Student 3)
Purpose: URL routing for the site_settings app.
Co-authors: None
"""

from django.urls import path
from . import views

app_name = 'site_settings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
]
