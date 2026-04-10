from django.contrib import admin

from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ("team_id", "team_name", "dept", "lead_user", "status")
	search_fields = ("team_name", "status", "dept__dept_name", "lead_user__username")
