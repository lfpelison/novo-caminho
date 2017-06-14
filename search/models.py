# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Article(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
