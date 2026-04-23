from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from organizations.models import Department
from teams.models import Team

import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# role based user filter
def get_visible_users(user):

    # department head
    if Department.objects.filter(manager=user).exists():
        dept = Department.objects.get(manager=user)
        return User.objects.filter(userprofile__department=dept)

    # team leader
    elif Team.objects.filter(lead_user=user).exists():
        team = Team.objects.get(lead_user=user)
        return User.objects.filter(userprofile__team=team)

   # normal user
    else:
        return User.objects.filter(id=user.id)


# main report page
@login_required
def report_view(request):
    users = get_visible_users(request.user)
    return render(request, "reports/summary.html", {"users": users})


# download excel
@login_required
def download_excel(request):
    users = get_visible_users(request.user)

    data = []
    for u in users:
        profile = getattr(u, "userprofile", None)

        data.append({
            "Username": u.username,
            "Email": u.email,
            "Team": str(profile.team) if profile and profile.team else "",
            "Department": str(profile.department) if profile and profile.department else "",
        })

    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

    df.to_excel(response, index=False)
    return response


# download pdf

@login_required
def download_pdf(request):
    users = get_visible_users(request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    content = []

    for u in users:
        text = f"{u.username} - {u.email}"
        content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)
    return response