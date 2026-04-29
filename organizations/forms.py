"""
Author: Eyup Okudan (w2117331)
Description: Constructs the DepartmentForm using Django's ModelForm.
Includes custom styling via Bootstrap classes and placeholders to ensure 
UI/UX consistency with the global design tokens[cite: 39, 41].
"""
from django import forms
# ... rest of your form code
from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'head_user']
        widgets = {
            'dept_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Engineering'}),
            # head_user'ı sildik çünkü o bir ForeignKey, 
            # Django otomatik olarak 'Select' kutusu yapmalı.
            'head_user': forms.Select(attrs={'class': 'form-control'}),
        }