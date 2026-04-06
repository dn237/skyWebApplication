from django.db import models

# Create your models here.
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name