from django.shortcuts import render
from .models import Department

# This function-based view retrieves all Department records from the database.
# It then passes this data to the HTML template for rendering.
def organization_list(request):
    # Fetching all entries from the Department table
    all_departments = Department.objects.all()
    
    # Passing the list of departments to the template via a context dictionary
    context = {
        'departments': all_departments
    }
    
    return render(request, 'organizations/organization_list.html', context)