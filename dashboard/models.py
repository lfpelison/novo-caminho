# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group
# Create your models here.

verified, created = Group.objects.get_or_create(name='verified')
