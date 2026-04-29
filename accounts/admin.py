# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django.contrib import admin
from .models import UserProfile

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # This shows you the User, their Team, and BOTH titles side-by-side
    list_display = ('user', 'team', 'job_title', 'role') 
    
    # Allows to quickly drill down into specific teams
    list_filter = ('team', 'department', 'job_title')
    
    # Makes it easy to find a specific person
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    # Optional: Groups fields logically when you click into a user
    fieldsets = (
        ('Identity', {
            'fields': ('user', 'avatar')
        }),
        ('Organizational Context', {
            'fields': ('team', 'department', 'job_title')
        }),
    )