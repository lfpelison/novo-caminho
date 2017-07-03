# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
### MONGO
import mongoengine as mg
from django_project.settings import MONGO_DBNAME

mg.connect(MONGO_DBNAME)

@python_2_unicode_compatible
class Article(mg.Document):
    url = mg.StringField(max_length=200, required=True)
    title = mg.StringField(max_length=200, required=True)
    short_summary = mg.StringField(max_length=200, required=True)
    long_summary = mg.StringField(max_length=500, required=True)
    publish_date = mg.DateTimeField(required=True)
    risk = mg.IntField()
    entities = mg.ListField()
    category = mg.StringField(max_length=20)
    def __str__(self):
        return "Titulo: {0}  ///  {1}".format(self.title,self.short_summary)
