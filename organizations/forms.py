from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'head_user']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Engineering'}),
            'head_user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}),
        }