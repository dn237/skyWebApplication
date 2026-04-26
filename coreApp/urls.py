"""
==========================================================================
DJANGO PROJECT STRUCTURE & TEAM ROLES
==========================================================================

[SYSTEM CENTER - CORE APP]
Role: Project Management & Global Settings.
Responsibility: Centralized configuration (settings.py) and main URL routing.
Note: Only edit this file when adding new apps or global middleware.
==========================================================================
Author: Diana Nichvolodova | Student ID: 20165015
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # For authentication

    path('', dashboard, name='dashboard'), # This makes dashboard the Home Page 
    path("teams/", include("teams.urls")),  # STUDENT 1
    path("organizations/", include("organizations.urls")),  # STUDENT 2 
    path("messages/", include("messaging.urls")),  # STUDENT 3
    path("schedules/", include("scheduler.urls")),  # STUDENT 4
    path("reports/", include("reports.urls")),  # STUDENT 5

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)