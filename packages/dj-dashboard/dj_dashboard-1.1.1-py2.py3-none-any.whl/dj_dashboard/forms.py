# -*- coding: utf-8 -*-
from django import forms
from .models import Dashboard


class DashboardForm(forms.ModelForm):
    """docstring for MassnahmenForm"""
    class Meta:
        model = Dashboard
        fields = ['widget_args', ]
