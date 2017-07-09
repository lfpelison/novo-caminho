# -*- coding: utf-8 -*-

from rest_framework import generics, permissions
from .serializers import ArticleSerializer
from search.models import Article
from django.shortcuts import render

class ArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        entities = self.kwargs['entities']
        return Article.objects.filter(entities__in=entities.split(","))

def index_API(request):
    return render(request, 'api/index_API.html')

#permission_classes = (permissions.IsAuthenticated,)
### Search the articles that contain the entities given.
