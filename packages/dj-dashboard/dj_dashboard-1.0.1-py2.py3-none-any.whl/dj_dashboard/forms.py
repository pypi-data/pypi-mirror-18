# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django import forms
from .models import Dashboard


class DashboardForm(forms.ModelForm):
    """docstring for MassnahmenForm"""
    class Meta:
        model = Dashboard
        fields = ['widget_args', ]
