"""
File: site_settings/views.py
Author: Yusuf (Student 3)
Purpose: View for the Settings page — renders and handles the 4-panel settings form.
Co-authors: None
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SitePreference
from messaging.models import MessagingPreference
from .forms import SitePreferenceForm, MessagingPreferenceForm


@login_required
def settings_view(request):
    site_pref, _ = SitePreference.objects.get_or_create(user=request.user)
    msg_pref, _  = MessagingPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        site_form = SitePreferenceForm(request.POST, instance=site_pref)
        msg_form  = MessagingPreferenceForm(request.POST, instance=msg_pref)
        if site_form.is_valid() and msg_form.is_valid():
            site_form.save()
            msg_form.save()
            messages.success(request, 'Settings saved.')
            return redirect('site_settings:settings')
    else:
        site_form = SitePreferenceForm(instance=site_pref)
        msg_form  = MessagingPreferenceForm(instance=msg_pref)

    return render(request, 'site_settings/settings.html', {
        'site_form': site_form,
        'msg_form': msg_form,
    })
