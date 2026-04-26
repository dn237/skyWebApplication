from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    report_type = models.CharField(max_length=50)

    time_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} report"