"""
File: site_settings/tests.py
Author: Yusuf (Student 3)
Purpose: Tests for the Settings page view and preference models.
Co-authors: None
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import SitePreference
from messaging.models import MessagingPreference

User = get_user_model()


class SettingsViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.url = reverse('site_settings:settings')

    def test_settings_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_settings_creates_preferences_on_first_visit(self):
        self.client.login(username='testuser', password='pass')
        self.client.get(self.url)
        self.assertTrue(SitePreference.objects.filter(user=self.user).exists())
        self.assertTrue(MessagingPreference.objects.filter(user=self.user).exists())

    def test_user_can_update_notification_preferences(self):
        self.client.login(username='testuser', password='pass')
        self.client.post(self.url, {
            'language': 'en-GB',
            'display_mode': 'light',
            'time_format': '12_GMT',
            # sound_notification intentionally omitted → unchecked checkbox → False
        })
        pref = MessagingPreference.objects.get(user=self.user)
        self.assertFalse(pref.sound_notification)

    def test_user_can_update_general_preferences(self):
        self.client.login(username='testuser', password='pass')
        self.client.post(self.url, {
            'language': 'en-GB',
            'display_mode': 'dark',
            'time_format': '12_GMT',
        })
        pref = SitePreference.objects.get(user=self.user)
        self.assertEqual(pref.display_mode, 'dark')
