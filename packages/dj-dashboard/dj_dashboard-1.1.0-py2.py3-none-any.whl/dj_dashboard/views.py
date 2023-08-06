# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

import json
from urllib.parse import parse_qs

from collections import OrderedDict

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .models import Dashboard
from .forms import DashboardForm


class BasisDashboardView(TemplateView):
    """"""
    template_name = "dj_dashboard.html"

    def dispatch(self, *args, **kwargs):
        """dispatch Used to have GET and POST on a TemplateView """
        return super(BasisDashboardView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BasisDashboardView, self).get_context_data(**kwargs)
        # set context config_mode
        if 'config_mode' in self.request.session and self.request.session['config_mode']:
            # Set the config_mode also in the context to show the configuration menu in the template
            context['config_mode'] = True
        else:
            # Disable the config_mode also in the context to disable the configuration menu in the template
            context['config_mode'] = False
        # if user has no dashboard configured for his user create a copy from the default one
        if Dashboard.objects.filter(
                user=self.request.user,
                dashboard_reverse_name=self.request.resolver_match.url_name).count() == 0:
            for widget in Dashboard.objects.filter(
                    user=None,
                    dashboard_reverse_name=self.request.resolver_match.url_name):
                widget.id = None
                widget.user = self.request.user
                widget.save_without_signals()
        # Load all Widgets from the model Widget. Needed for the configuration form
        context['widgetlist'] = []
        # Create a sortet by: GROUP_NAME, WIDGET_CLASS, TITLE
        constants_widgetlist = OrderedDict(sorted(settings.DJ_DASH_WIDGETS.items(),
                                                  key=lambda x: ('%s%s%s') % (x[1][2],
                                                                              x[1][1],
                                                                              x[1][0])))
        for key, value in constants_widgetlist.items():
            widget_data = {}
            widget_data['name'] = value[0]
            widget_data['group'] = settings.DJ_DASH_WIDGETGROUPS[value[2]][0]
            widget_data['group_class'] = settings.DJ_DASH_WIDGETGROUPS[value[2]][1]
            widget_data['widget_class_name'] = settings.DJ_DASH_WIDGETCLASSES[value[1]][0]
            widget_data['widget_class'] = settings.DJ_DASH_WIDGETCLASSES[value[1]][1]
            widget_data['reverse_name'] = key
            context['widgetlist'].append(widget_data)

        # We create an array which contains dictoniaries with the widget data like position, url, ...
        widgets = []
        # We filter all widgets for the actual user on this dashboard.
        # We need them ordered like they should be displayed becasue gridstack addWidget needs
        #  to be executed in this order or some widgets will be moved down and we have a free space
        #  on the page
        for dashboard in Dashboard.objects.filter(
                user=self.request.user,
                dashboard_reverse_name=self.request.resolver_match.url_name).order_by(
                'position_y', 'id', 'position_x'):
            widget = {}
            if dashboard.widget_reverse_name and dashboard.widget_reverse_name > '':
                widget['id'] = dashboard.id
                # TODO: rename field
                widget['reverse_name'] = dashboard.widget_reverse_name
                widget['url'] = reverse(dashboard.widget_reverse_name)
                widget['edit_reverse_name'] = ""
                widget['edit_url'] = ""
                if dashboard.user:
                    widget['user_id'] = dashboard.user_id
                else:
                    widget['user_id'] = None
                if dashboard.enable_edit:
                    # If this Widgets has an update view to set filter, the link goes here
                    widget['edit_reverse_name'] = "%s-update/" % dashboard.widget_reverse_name
                    widget['edit_url'] = "%s%s/update?_popup=1" % (widget['url'], widget['id'])
                if dashboard.widget_args and len(dashboard.widget_args) > 0:
                    widget['args'] = "?%s" % dashboard.widget_args
                    if dashboard.enable_edit:
                        widget['edit_url'] += "&%s" % dashboard.widget_args
                widget['x'] = dashboard.position_x
                widget['y'] = dashboard.position_y
                widget['w'] = dashboard.width
                widget['h'] = dashboard.height
                # Append to widgets
                widgets.append(widget)
        context['widgets'] = widgets

        # We are used to set DEBUG in django setting so we check this here. If there is no DEBUG
        #  it is false
        try:
            context['django_debug'] = settings.DEBUG
        except:
            logger.info("Missing DEBUG in dajngo settings.")
            context['django_debug'] = False
        return context

    def post(self, request, *args, **kwargs):
        # Reset to de default dashboard
        if 'reset-default' in self.request.POST and self.request.POST['reset-default'] == '1':
            logger.debug("Reset to the default dashboard for the user '%s' " % self.request.user)
            Dashboard.objects.filter(
                user=self.request.user,
                dashboard_reverse_name=self.request.resolver_match.url_name,).delete()
        else:
            # Delete widgets from the Dashboard
            if 'remove-widget' in self.request.POST and self.request.POST['remove-widget']:
                remove_widgets = self.request.POST.getlist('remove-widget', [])
                logger.debug("Removing this widgets with id's '%s' from the Dashbord" % remove_widgets)
                Dashboard.objects.filter(id__in=remove_widgets).delete()

            # If there is a new Widget to add, add this
            if self.request.POST['add-widget-select']:
                logger.debug("Adding the new widget '%s' to the dashbaord '%s'" %
                             (self.request.POST['add-widget-select'],
                              self.request.resolver_match.url_name))
                try:
                    reverse(self.request.POST['add-widget-select'])
                    dashboard_widget = Dashboard.objects.create(
                        user=self.request.user,
                        dashboard_reverse_name=self.request.resolver_match.url_name,
                        widget_reverse_name=self.request.POST['add-widget-select'],
                        position_y=self.request.POST['add-widget-y'])
                except:
                    logger.debug("Dropped not valid component. Resolv for '%s' not possibile" % self.request.POST['add-widget-select'])
            else:
                # Get Data from the Post. Witgets is a JSon Type
                widgets = json.loads(self.request.POST['widgets'])
                # Update all Widgets saving position, width, height
                for widget in widgets:
                    if Dashboard.objects.filter(id=widget['id']).exists():
                        dashboard_widget = Dashboard.objects.get(id=widget['id'])
                        dashboard_widget.position_x = widget['x']
                        dashboard_widget.position_y = widget['y']
                        dashboard_widget.width = widget['width']
                        dashboard_widget.height = widget['height']
                        dashboard_widget.save()
        return


class BasisDashboardUpdateView(UpdateView):
    """"""
    model = Dashboard
    form_class = DashboardForm

    def get_initial(self):
        if not self.initial:
            self.initial = {}

        for key in self.object.__dict__.keys():
            if key == 'widget_args' and self.object.widget_args:
                widget_arg = parse_qs(self.object.widget_args)
                for key in widget_arg.keys():
                    if key == 'chart_type':
                        self.initial.update({key: widget_arg[key][0]})
                    else:
                        self.initial.update({key: widget_arg[key]})
            else:
                self.initial.update({key: self.object.__dict__[key]})
        return self.initial
