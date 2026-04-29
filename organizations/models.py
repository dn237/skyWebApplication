# organizations/models.py
from django.db import models
from django.conf import settings

class Department(models.Model):
    dept_name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Department Name"
    )
    
    # manager: Restored from CharField to ForeignKey using a string reference 
    # to solve the circularity issue mentioned in peer feedback.
    head_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name="Head of Department"
    )

    def __str__(self):
        return self.dept_name