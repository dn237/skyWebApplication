"""
File: site_settings/forms.py
Author: Yusuf (Student 3)
Purpose: Forms for the Settings page — general preferences and messaging preferences.
Co-authors: None
"""

from django import forms
from .models import SitePreference
from messaging.models import MessagingPreference


class SitePreferenceForm(forms.ModelForm):
    class Meta:
        model = SitePreference
        fields = ['language', 'display_mode', 'time_format']
        widgets = {
            'language': forms.Select(),
            'display_mode': forms.Select(),
            'time_format': forms.Select(),
        }


class MessagingPreferenceForm(forms.ModelForm):
    class Meta:
        model = MessagingPreference
        fields = ['email_notification', 'sound_notification', 'do_not_disturb']
        widgets = {
            'email_notification': forms.CheckboxInput(),
            'sound_notification': forms.CheckboxInput(),
            'do_not_disturb': forms.CheckboxInput(),
        }
