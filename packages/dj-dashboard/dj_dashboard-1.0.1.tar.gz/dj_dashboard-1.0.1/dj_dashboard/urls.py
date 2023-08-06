# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import BasisDashboardView, BasisDashboardUpdateView

urlpatterns = [
    url(r'^dj_dashboard/$', login_required(BasisDashboardView.as_view()), name='dj_dashboard'),
    url(r'^dj_dashboard/(?P<pk>[0-9]+)/update/$', login_required(BasisDashboardUpdateView.as_view()), name='dj_dashboard-update'),
]
