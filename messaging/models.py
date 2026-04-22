from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_messages')

    text = models.TextField()

    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
    ])

    time_sent = models.DateTimeField(auto_now_add=True)
    time_received = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text[:20]