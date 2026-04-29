"""
File: site_settings/admin.py
Author: Yusuf (Student 3)
Purpose: Admin registration for the SitePreference model.
Co-authors: None
"""

from django.contrib import admin
from .models import SitePreference


@admin.register(SitePreference)
class SitePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'display_mode', 'time_format')
