# reports/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from organizations.models import Department
from teams.models import Team

import pandas as pd

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# filter by role
def get_visible_users(user):

    # admin
    if user.is_superuser:
        return User.objects.all()

    # department head
    dept = Department.objects.filter(head_user=user).first()
    if dept:
        return User.objects.filter(profile__team__dept=dept)

    # team leader
    team = Team.objects.filter(lead_user=user).first()
    if team:
        return User.objects.filter(profile__team=team)

    # normal user
    return User.objects.filter(id=user.id)


# build structure
def build_structure(users):
    structure = {}

    for u in users:
        profile = getattr(u, "profile", None)

        team = profile.team if profile and profile.team else None
        dept = team.dept if team and hasattr(team, "dept") else None

        dept_name = str(dept) if dept else "Unassigned"
        team_name = str(team) if team else "No Team"

        if dept_name not in structure:
            structure[dept_name] = {
                "manager": dept.head_user if dept else None,
                "teams": {}
            }

        if team_name not in structure[dept_name]["teams"]:
            structure[dept_name]["teams"][team_name] = {
                "leader": getattr(team, "lead_user", None) if team else None,
                "users": []
            }

        structure[dept_name]["teams"][team_name]["users"].append(u)

    # sort users A-Z
    for dept in structure.values():
        for team in dept["teams"].values():
            team["users"].sort(key=lambda x: x.username.lower())

    # move "Unassigned" to bottom
    structure = dict(sorted(structure.items(), key=lambda x: x[0] == "Unassigned"))

    return structure


# main view
@login_required
def report_view(request):
    users = get_visible_users(request.user).select_related("profile")
    structure = build_structure(users)

    return render(request, "reports/summary.html", {
        "structure": structure
    })


# excel export
@login_required
def download_excel(request):
    users = get_visible_users(request.user).select_related("profile")

    data = []

    for u in users:
        profile = getattr(u, "profile", None)

        team = profile.team if profile else None
        dept = team.dept if team else None

        data.append({
            "Department": str(dept) if dept else "Unassigned",
            "Manager": dept.head_user if dept else "",
            "Team": str(team) if team else "No Team",
            "Team Leader": getattr(team, "lead_user", "") if team else "",
            "Username": u.username,
            "Email": u.email,
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="team_report.xlsx"'

    # Requires 'openpyxl' installed in your .venv
    df.to_excel(response, index=False) # type: ignore
    return response


# pdf export
@login_required
def download_pdf(request):
    users = get_visible_users(request.user).select_related("profile")
    structure = build_structure(users)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="staff_report.pdf"'

    doc = SimpleDocTemplate(response) # type: ignore
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Staff Visibility Report", styles["Title"]))

    for dept_name, dept_data in structure.items():

        content.append(Paragraph(f"<b>Department:</b> {dept_name}", styles["Heading2"]))
        content.append(Paragraph(f"Manager: {dept_data['manager'] or 'Unassigned'}", styles["Normal"]))
        content.append(Spacer(1, 10))

        for team_name, team_data in dept_data["teams"].items():

            content.append(Paragraph(f"<b>Team:</b> {team_name}", styles["Heading3"]))
            content.append(Paragraph(f"Leader: {team_data['leader'] or 'Unassigned'}", styles["Normal"]))

            for u in team_data["users"]:
                email_part = f" ({u.email})" if u.email else ""
                content.append(Paragraph(f"- {u.username}{email_part}", styles["Normal"]))

            content.append(Spacer(1, 12))

        content.append(Spacer(1, 20))

    doc.build(content)
    return response