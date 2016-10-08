# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import datetime

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    staged = models.DateTimeField(null = True, blank = True)

    def __init__(self, *args, **kwargs):
        super(AbstractUser,self).__init__(*args, **kwargs)
        if self.staged is None and self.date_joined < timezone.now() - datetime.timedelta(days = 1):
            self.staged = timezone.now()
            self.save()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
