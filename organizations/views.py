from django.shortcuts import render, get_object_or_404
from .models import Department
from django.db.models import Q

# Updated List View with Search Logic
def organization_list(request):
    # Get the search query from the URL (e.g., /organizations/?q=mobile)
    query = request.GET.get('q')
    
    if query:
        # Filter departments if their name or head_user contains the query string (case-insensitive)
        departments = Department.objects.filter(
            Q(dept_name__icontains=query) | Q(head_user__icontains=query)
        )
    else:
        # If no search, show all departments
        departments = Department.objects.all()
    
    return render(request, 'organizations/organization_list.html', {
        'departments': departments,
        'query': query # Sending query back to show it in the search box
    })

# Detail View remains the same, using dept.html
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'organizations/dept.html', {
        'department': department
    })