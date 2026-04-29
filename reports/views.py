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

    # admin/superuser
    if user.is_superuser:
        return User.objects.all()

    # department head
    dept = Department.objects.filter(head_user=user).first()
    if dept:
        return User.objects.filter(profile__department=dept)

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

        dept_name = str(profile.department) if profile and profile.department else "No Department"
        team_name = str(profile.team) if profile and profile.team else "No Team"

        if dept_name not in structure:
            structure[dept_name] = {
                "manager": getattr(profile.department, "head_user", None) if profile and profile.department else None,
                "teams": {}
            }

        if team_name not in structure[dept_name]["teams"]:
            structure[dept_name]["teams"][team_name] = {
                "leader": getattr(profile.team, "lead_user", None) if profile and profile.team else None,
                "users": []
            }

        structure[dept_name]["teams"][team_name]["users"].append(u)

    # sort users A-Z
    for dept in structure.values():
        for team in dept["teams"].values():
            team["users"].sort(key=lambda x: x.username.lower())

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

        dept = profile.department if profile else ""
        team = profile.team if profile else ""

        leader = getattr(team, "lead_user", None) if team else ""
        manager = getattr(dept, "head_user", None) if dept else ""

        data.append({
            "Department": str(dept),
            "Manager": str(manager),
            "Team": str(team),
            "Team Leader": str(leader),
            "Username": u.username,
            "Email": u.email,
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    df.to_excel(response, index=False)
    return response


# pdf export
@login_required
def download_pdf(request):
    users = get_visible_users(request.user).select_related("profile")
    structure = build_structure(users)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    for dept_name, dept_data in structure.items():

        content.append(Paragraph(f"<b>Department:</b> {dept_name}", styles["Heading2"]))

        manager = dept_data["manager"]
        content.append(Paragraph(f"Manager: {manager or '-'}", styles["Normal"]))
        content.append(Spacer(1, 10))

        for team_name, team_data in dept_data["teams"].items():

            content.append(Paragraph(f"<b>Team:</b> {team_name}", styles["Heading3"]))

            leader = team_data["leader"]
            content.append(Paragraph(f"Leader: {leader or '-'}", styles["Normal"]))

            for u in team_data["users"]:
                content.append(Paragraph(f"- {u.username} ({u.email})", styles["Normal"]))

            content.append(Spacer(1, 12))

        content.append(Spacer(1, 20))

    doc.build(content)
    return response