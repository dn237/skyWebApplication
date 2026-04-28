"""Forms used by the accounts app."""

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile

# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================


class CustomUserCreationForm(UserCreationForm):
    """Signup form with a few extra user fields."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({
                'class': 'form-control sky-input',
                'placeholder': f'Enter {self.fields[fieldname].label}'
            })


class ProfileAvatarForm(forms.ModelForm):
    """Form for uploading a profile picture."""
    class Meta:
        model = UserProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*'
        })