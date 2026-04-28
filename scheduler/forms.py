from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['title', 'message', 'date', 'time', 'platform', 'schedule_type']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Enter title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'custom-input',
                'placeholder': 'Add description...'
            }),
            'platform': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Zoom / Teams / etc'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'custom-input'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'custom-input'
            }),
}