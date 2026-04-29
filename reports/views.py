# reports/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from organizations.models import Department
from teams.models import Team

import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ========================================================
# ROLE-BASED USER FILTER
# ========================================================
def get_visible_users(user):
    """
    Determines which users a logged-in person is allowed to see 
    based on their organizational role.
    """
    
    # This ensures admins aren't restricted by the role-based filters below
    if user.is_superuser or user.is_staff:
        return User.objects.all()
    
    # 1. Check if user is a Department Head
    # Using 'head_user' to match the refactored Department model.
    # We pass the 'user' object directly to satisfy the ForeignKey requirement.
    if Department.objects.filter(head_user=user).exists():
        dept = Department.objects.get(head_user=user)
        # Return all users belonging to any team under this department
        return User.objects.filter(profile__team__dept=dept)

    # 2. Check if user is a Team Leader
    elif Team.objects.filter(lead_user=user).exists():
        team = Team.objects.get(lead_user=user)
        # Return all users belonging to this specific team
        return User.objects.filter(profile__team=team)

    # 3. Normal Staff User
    else:
        # Return only the user's own record
        return User.objects.filter(id=user.id)


# ========================================================
# VIEWS
# ========================================================

@login_required
def report_view(request):
    """Main summary page showing visible users."""
    users = get_visible_users(request.user)
    return render(request, "reports/summary.html", {"users": users})


@login_required
def download_excel(request):
    """Generates an Excel export of visible users."""
    users = get_visible_users(request.user)

    data = []
    for u in users:
        # Using getattr to safely handle users without profiles
        profile = getattr(u, "profile", None)

        data.append({
            "Username": u.username,
            "Email": u.email,
            "Team": str(profile.team) if profile and profile.team else "N/A",
            "Department": str(profile.team.dept) if profile and profile.team and profile.team.dept else "N/A",
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="team_report.xlsx"'

    # Requires 'openpyxl' installed in your .venv
    df.to_excel(response, index=False) # type: ignore
    return response


@login_required
def download_pdf(request):
    """Generates a PDF export of visible users."""
    users = get_visible_users(request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="staff_report.pdf"'

    doc = SimpleDocTemplate(response) # type: ignore
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Staff Visibility Report", styles["Title"]))

    for u in users:
        profile = getattr(u, "profile", None)
        team_name = str(profile.team) if profile and profile.team else "No Team"
        text = f"<b>User:</b> {u.username} | <b>Email:</b> {u.email} | <b>Team:</b> {team_name}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)
    return response