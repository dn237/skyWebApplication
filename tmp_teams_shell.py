# ================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# Co-author: COPILOT
# ----->
from django.test import Client
c = Client()
cases = [("search", "/teams/?q=API"), ("dept", "/teams/?departments=Arch")]
for label, url in cases:
    r = c.get(url)
    body = r.content.decode("utf-8", "replace")
    print(label, "status=", r.status_code, "no_teams_found=", ("No teams found." in body), "card_count=", body.count('<div class="card card-item">'))
# =================================================