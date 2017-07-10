# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import utils
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
import json

### MONGO
import mongoengine as mg
from django_project.settings import MONGO_DATABASE

mg.connect(
    db=         MONGO_DATABASE['db'],
    username=   MONGO_DATABASE['username'],
    password=   MONGO_DATABASE['password'],
    host=       MONGO_DATABASE['host'],
)

    
@python_2_unicode_compatible
class Article(mg.Document):
    url = mg.StringField(max_length=200, required=True, validators=[MinLengthValidator(1)])
    title = mg.StringField(max_length=200, required=True, validators=[MinLengthValidator(1)])
    short_summary = mg.StringField(max_length=200, required=True, validators=[MinLengthValidator(1)])
    long_summary = mg.StringField(max_length=500, required=True, validators=[MinLengthValidator(1)])
    publish_date = mg.DateTimeField()
    risk = mg.IntField()
    entities = mg.ListField()
    category = mg.StringField(max_length=20)
    def __str__(self):
        return "URL: {0}\n".format(self.url)

    def fill_and_create(self, article, entities, risk, category):
        if article.title != "" and article.summary != "" and article.url != "":
            self.url=article.url
            self.short_summary=article.summary[:200]
            self.long_summary=article.summary
            self.title=article.title
            self.entities= entities
            self.publish_date= article.publish_date
            self.risk = risk
            self.category = category
            self.save()
            return self
        else:
            return None


@python_2_unicode_compatible  # only if you need to support Python 2
class Query(models.Model):
    name = models.CharField(max_length=200, blank=False)
    time = models.DateTimeField('date searched', default=utils.timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
     # JSON-serialized (text) version of the list
    entities = models.TextField(null=True)
    engines = models.TextField(null=True)
    def __str__(self):
        return "User: {0}, Name: {1}, Time: {2}, Entities: {3}, Engines: {4}".format(str(self.user), self.name, str(self.time), str(self.entities), str(self.engines))

    def get_engines(self):
        return self.get('engines')

    def get_entities_formated(self):
        return ",".join(self.get('entities'))

    def get(self, field):
        return json.JSONDecoder().decode(getattr(self, field))

    def set(self, field, list):
        setattr(self, field, json.dumps(list))

@python_2_unicode_compatible
class Keyword(models.Model):
    name = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Name: {0}, User{1}".format(self.name,self.user)

@python_2_unicode_compatible
class IgnoredDomain(models.Model):
    name = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Name: {0}, User{1}".format(self.name,self.user)
