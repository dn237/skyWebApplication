"""
File: messaging/forms.py
Author: Yusuf (Student 3)
Purpose: Form for composing messages.
Co-authors: None
"""

from django import forms
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['recipient'].queryset = (
                User.objects.exclude(id=user.id).order_by('first_name', 'username')
            )
        self.fields['recipient'].required = False
