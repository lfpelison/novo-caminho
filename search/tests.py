# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from search.models import *

class SearchModelsTestCase(TestCase):
    def setUp(self):
        u=User.objects.create(username='jeff')
        q=Query.objects.create(user=u)
        e=Entity.objects.create()

    def test_relations(self):
        q = Query.objects.first()
        u = User.objects.first()
        e = Entity.objects.first()
        e.query_set.add(q)
        self.assertEqual(q.user, u)
        self.assertEqual(q,e.query_set.first())
        self.assertEqual(e,q.entity.first())
