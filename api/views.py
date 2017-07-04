# -*- coding: utf-8 -*-

from rest_framework import generics
from .serializers import ArticleSerializer
from search.models import Article

class ArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        entities = self.kwargs['entities']
        return Article.objects.filter(entities=entities.split(","))

### Search the articles that contain the entities given.
