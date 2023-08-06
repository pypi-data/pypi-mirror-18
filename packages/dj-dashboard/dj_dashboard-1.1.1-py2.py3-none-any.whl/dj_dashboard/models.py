# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save

from model_utils.models import TimeStampedModel


class Dashboard(TimeStampedModel):
    """docstring for Dashboard"""
    dashboard_reverse_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Dashboard reverse name')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, default=None, related_name='%(app_label)s_%(class)s_users', verbose_name=_('User'))
    position_y = models.IntegerField(blank=True, default=0, verbose_name='Element position Y')
    position_x = models.IntegerField(blank=True, default=0, verbose_name='Element position X')
    width = models.IntegerField(blank=True, default=12, verbose_name=_('Widget width'))
    height = models.IntegerField(blank=True, default=2, verbose_name=_('Widget height'))
    widget_reverse_name = models.CharField(max_length=300, blank=True, null=True, verbose_name='Content reverse name')
    widget_args = models.CharField(max_length=300, blank=True, null=True, verbose_name='Content args')
    enable_edit = models.BooleanField(default=True, verbose_name=_('Enable Edit'))

    class Meta:
        verbose_name = _('Dashboard')
        verbose_name_plural = _('Dashboards')

    def save_without_signals(self):
        """
        This allows for updating the model from code running inside post_save()
        signals without going into an infinite loop:
        http://stackoverflow.com/questions/10840030/django-post-save-preventing-recursion-without-overriding-model-save
        """
        self._signals = False
        self.save()
        self._signals = True


@receiver(post_save, sender=Dashboard)
def post_save_dashboard(sender, instance, created, **kwargs):
    if getattr(instance, '_signals', True) and created and instance.user:
        Dashboard.objects.filter(
            dashboard_reverse_name=instance.dashboard_reverse_name,
            user=instance.user).exclude(id=instance.id).update(position_y=F('position_y') + 2)
