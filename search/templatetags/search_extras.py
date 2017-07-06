import urllib
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs): # same as 'url' but keeps the GET data => /users/?sort_by=name => <a href=url_replace 'items'> => /items/?sort_by=name
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urllib.urlencode(query)
