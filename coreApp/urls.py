"""
==========================================================================
DJANGO PROJECT STRUCTURE & TEAM ROLES
==========================================================================

[SYSTEM CENTER - CORE APP]
Role: Project Management & Global Settings.
Responsibility: Centralized configuration (settings.py) and main URL routing.
Note: Only edit this file when adding new apps or global middleware.

--------------------------------------------------------------------------
[STUDENT MODULES - ASSIGNMENTS]

1. STUDENT 1: Teams Management
   Path: /teams/
   Tasks: Team lists, search, email contacts, skills, and dependencies.

2. STUDENT 2: Organization & Departments
   Path: /organizations/
   Tasks: Department hierarchy, team types, and visual mapping.

3. STUDENT 3: Private Messaging
   Path: /messages/
   Tasks: Inbox, Sent, Drafts, and composing new messages.

4. STUDENT 4: Meeting Scheduler
   Path: /schedules/
   Tasks: Calendar views (Month/Week), Zoom/Teams integration, timestamps.

5. STUDENT 5: Management Reports
   Path: /reports/
   Tasks: PDF/Excel generation, team summaries, manager-less team audits.
==========================================================================
"""

from django.contrib import admin
from django.urls import include, path

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