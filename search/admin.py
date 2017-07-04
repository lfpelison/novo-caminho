# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Query, Entity

admin.site.register(Query)
admin.site.register(Entity)

# Register your models here.
