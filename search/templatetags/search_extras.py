import urllib
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs): # same as 'url' but keeps the GET data => /users/?sort_by=name => <a href=url_replace 'items'> => /items/?sort_by=name
    query = context['request'].GET.dict()
    query.update(kwargs)
    url = urllib.urlencode(query)
    return "?"+url

@register.simple_tag(takes_context=True)
def goto_page(context, number, **kwargs):
    return url_replace(context, page=number)

@register.simple_tag(takes_context=True)
def prev_page(context, **kwargs):
    return url_replace(context, page=context['page']-1)


@register.simple_tag(takes_context=True)
def next_page(context, **kwargs):
    return url_replace(context, page=context['page']+1)
