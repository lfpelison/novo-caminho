# -*- coding: utf-8 -*-

from rest_framework import generics, permissions
from .serializers import ArticleSerializer
from search.models import Article

class ArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        entities = self.kwargs['entities']
        return Article.objects.filter(entities__in=entities.split(","))

permission_classes = (permissions.IsAuthenticated,)
### Search the articles that contain the entities given.
