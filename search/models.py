# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import utils
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


@python_2_unicode_compatible  # only if you need to support Python 2
class Entity(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return "Entity Name: {0}, Entity ID: {1}, Query: {2}".format(self.name, str(self.id), str(self.query_set))


@python_2_unicode_compatible  # only if you need to support Python 2
class Query(models.Model):
    name = models.CharField(max_length=200, blank=False)
    time = models.DateTimeField('date searched', default=utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity = models.ManyToManyField(Entity)

    def __str__(self):
        return "User ID: {0}, Name: {1}, Searched: {2}, Query ID: {3}".format(str(self.user), self.name, str(self.time), str(self.id))
