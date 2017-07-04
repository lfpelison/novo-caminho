# -*- coding: utf-8 -*-

from rest_framework import serializers
from search.models import Article

class ArticleSerializer(serializers.Serializer):
    url = serializers.URLField(read_only=True)
    title = serializers.CharField(read_only=True)
    short_summary = serializers.CharField(read_only=True)
    long_summary = serializers.CharField(read_only=True)
    publish_date = serializers.CharField(read_only=True)
    risk = serializers.IntegerField(read_only=True)
    entities = serializers.ListField(read_only=True)
    category = serializers.CharField(read_only=True)
