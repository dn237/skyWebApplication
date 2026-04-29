"""
File: messaging/admin.py
Author: Yusuf (Student 3)
Purpose: Admin registration for the Message model.
Co-authors: None
"""

from django.contrib import admin
from .models import Message, MessagingPreference


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('subject', 'body', 'sender__username', 'recipient__username')


@admin.register(MessagingPreference)
class MessagingPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notification', 'sound_notification', 'do_not_disturb')
