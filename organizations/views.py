from django.shortcuts import render, get_object_or_404
from .models import Department
from django.db.models import Q
from django.shortcuts import redirect
from .forms import DepartmentForm
from django.contrib import messages

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

def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department successfully added!')
            return redirect('organizations:dept') # Kaydedince listeye geri dön
    else:
        form = DepartmentForm()
    
    return render(request, 'organizations/department_form.html', {'form': form})
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        # formun içine 'instance=department' vererek mevcut bilgileri yüklüyoruz
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'{department.dept_name} successfully updated!')
            return redirect('organizations:detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    # Mevcut department_form.html'i tekrar kullanıyoruz, ekstra dosya açmaya gerek yok
    return render(request, 'organizations/department_form.html', {'form': form, 'department': department})
def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department_name = department.dept_name
        department.delete()
        # Silme işlemi sonrası listeye dön ve uyarı mesajı ver
        messages.success(request, f'{department_name} successfully deleted!')
        return redirect('organizations:dept')
    
    # Eğer GET isteği gelirse onay sayfasına gönder
    return render(request, 'organizations/department_confirm_delete.html', {'department': department})