"""
File: messaging/context_processors.py
Author: Yusuf (Student 3)
Purpose: Injects unread message data into every template context.
"""
from .models import Message


def messaging_context(request):
    if not request.user.is_authenticated:
        return {}
    unread_qs = Message.objects.filter(
        recipient=request.user,
        status='sent',
        read_at__isnull=True,
    )
    recent_unread = list(unread_qs.select_related('sender').order_by('-created_at')[:5])
    return {
        'recent_unread_messages': recent_unread,
        'unread_count': unread_qs.count(),
    }
