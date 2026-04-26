"""
File: messaging/models.py
Author: Yusuf (Student 3)
Purpose: Message model for internal direct messaging system
"""

from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ]

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='received_messages'
    )

    subject = models.CharField(max_length=200, default='')
    body = models.TextField(default='')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Keep old fields for backward compatibility with existing data
    text = models.TextField(blank=True, default='')
    time_sent = models.DateTimeField(auto_now_add=True)
    time_received = models.DateTimeField(null=True, blank=True)

    # New fields
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-time_sent']

    def __str__(self):
        return f"{self.subject or '(no subject)'} - {self.sender}"