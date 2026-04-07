from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name