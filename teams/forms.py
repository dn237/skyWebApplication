from django import forms
from .models import TeamUpdate


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = TeamUpdate
        fields = ('title', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Update title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the update...'}),
        }
# =================================================
# AUTHOR: DIANA NICHVOLODOVA | STUDENT ID: 20165015
# =================================================

from django import forms
from .models import Team


class TeamForm(forms.ModelForm):
    REQUIRED_FIELDS = {
        'team_name',
        'focus_areas',
        'dept',
        'lead_user',
        'skills_technologies',
    }

    STATUS_CHOICES = [
        ('', 'Select Status'),
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    class Meta:
        model = Team
        fields = [
            'team_name', 
            'mission_statement', 
            'workstream_mf', 
            'focus_areas', 
            'skills_technologies',
            'slack_channels',
            'standup_details',
            'agile_practices',
            'team_wiki',
            'github_url',
            'jira_board_link',
            'status',
            'dept',
            'lead_user'
        ]
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'mission_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mission Statement'}),
            'workstream_mf': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'focus_areas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'skills_technologies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'slack_channels': forms.TextInput(attrs={'class': 'form-control'}),
            'standup_details': forms.TextInput(attrs={'class': 'form-control'}),
            'agile_practices': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'team_wiki': forms.TextInput(attrs={'class': 'form-control'}),
            'github_url': forms.TextInput(attrs={'class': 'form-control'}),
            'jira_board_link': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'dept': forms.Select(attrs={'class': 'form-control'}),
            'lead_user': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only selected fields should be mandatory in the edit form.
        for name, field in self.fields.items():
            field.required = name in self.REQUIRED_FIELDS
