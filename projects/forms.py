from django import forms
# from django.contrib.auth.models import User
from tempus_dominus.widgets import DatePicker
from .models import Project, Attachment
from teams.models import Team
from .utils import STATUS_CHOICES, PRIORITY_CHOICES

class ProjectForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': "Describe your project here ..."}
        ),
        label=False,
        required=True
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Enter the name of your project here ..."}
        ),
        required=True,
        label=False
    )

    # owner = forms.ModelChoiceField(
    #     queryset= User.objects.filter(is_active=True),
    #     widget=forms.Select(
    #         attrs={'class': "form-control"}
    #     ),
    #     label=False,
    #     required=True
    # )

    team = forms.ModelChoiceField(
        queryset= Team.objects.all(),
        widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label=False,
        required=True
    )

    client_company = forms.CharField(
        label=False,
        required=True
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
       widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label=False,
        required=True
    )


    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
       widget=forms.Select(
            attrs={'class': "form-control"}
        ),
        label=False,
        required=True
    )

    start_date = forms.DateTimeField(
        label=False,
        required=True,
        widget=DatePicker(
            attrs = {
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    due_date = forms.DateTimeField(
        label=False,
        required=True,
        widget=DatePicker(
            attrs = {
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    total_amount = forms.DecimalField(
        label=False,
        required=False
    )

    amount_spent = forms.DecimalField(
        label=False,
        required=False
    )

    estimated_duration = forms.DecimalField(
        label=False,
        required=False
    )


    class Meta:
        model = Project
        fields = [
            "name", 
            "team", 
            "client_company", 
            "description", 
            "status", 
            "priority", 
            "start_date", 
            "due_date",
            "total_amount",
            "amount_spent",
            "estimated_duration"
            ]

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']