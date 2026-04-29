"""
File: site_settings/models.py
Author: Yusuf (Student 3)
Purpose: Defines the SitePreference model for per-user application settings.
Co-authors: None
"""

from django.db import models
from django.conf import settings


class SitePreference(models.Model):
    LANGUAGE_CHOICES = [
        ('en-GB', 'English (United Kingdom)'),
        ('en-US', 'English (United States)'),
    ]
    DISPLAY_CHOICES = [
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
    ]
    TIME_CHOICES = [
        ('12_GMT', '12 hour, GMT'),
        ('24_GMT', '24 hour, GMT'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='site_prefs'
    )
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='en-GB')
    display_mode = models.CharField(max_length=10, choices=DISPLAY_CHOICES, default='light')
    time_format = models.CharField(max_length=20, choices=TIME_CHOICES, default='12_GMT')

    def __str__(self):
        return f"SitePreference({self.user})"
