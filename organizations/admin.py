from django.contrib import admin
from .models import Department

# Registering the Department model to make it accessible in the Django Admin panel.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # CORRECTED: Changed 'manager' to 'head_user' to match the model definition.
    list_display = ('id', 'dept_name', 'head_user')
    
    # Enables a search bar to find departments by name.
    search_fields = ('dept_name',)
    
    # Optional: adds an ordering rule (ascending by name).
    ordering = ('dept_name',)