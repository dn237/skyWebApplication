from django.contrib import admin
from .models import Department

# Using the decorator is the modern and "proper" way to register.
# It links the Department model with the DepartmentAdmin customization class.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # display the ID, Name and Head in the list view
    list_display = ('id', 'dept_name', 'head_user')
    
    # adds a search bar for department names
    search_fields = ('dept_name',)
    
    # orders the list by name by default
    ordering = ('dept_name',)

# REMOVED: admin.site.register(Department) <- This would cause an AlreadyRegistered error.