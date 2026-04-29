"""
Author: Eyup Okudan (w2117331)
Description: Manages the business logic for organizational units, including:
- organization_list: Handles department listing and keyword search.
- create_department: Processes the addition of new departments.
- edit_department: Manages updates to existing department records.
- delete_department: Handles the removal of records with confirmation.
- department_detail: Displays specific information for a single department.
"""
from django.shortcuts import render, get_object_or_404, redirect
# ... rest of your imports and views
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm

# Updated List View with Search Logic
def organization_list(request):
    # Get the search query from the URL (e.g., /organizations/?q=mobile)
    query = request.GET.get('q')
    
    if query:
        # FIX: Filter departments by dept_name or the related user's username/first_name
        departments = Department.objects.filter(
            Q(dept_name__icontains=query) | 
            Q(head_user__username__icontains=query) |
            Q(head_user__first_name__icontains=query)
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

def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department successfully added!')
            # Redirecting to the list view after a successful save
            return redirect('organizations:organization_list') 
    else:
        form = DepartmentForm()
    
    return render(request, 'organizations/department_form.html', {'form': form})

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        # Load existing instance into the form for updating
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'{department.dept_name} successfully updated!')
            return redirect('organizations:detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    # Reuse existing department_form.html for editing
    return render(request, 'organizations/department_form.html', {'form': form, 'department': department})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department_name = department.dept_name
        department.delete()
        # Redirect to the list view after deletion and display a success message
        messages.success(request, f'{department_name} successfully deleted!')
        return redirect('organizations:organization_list')
    
    # If GET request, send to the confirmation page
    return render(request, 'organizations/department_confirm_delete.html', {'department': department})