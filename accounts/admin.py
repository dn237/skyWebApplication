# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.contrib import admin
from .models import UserProfile

# Keep the profile model easy to manage from the admin site.
admin.site.register(UserProfile)
