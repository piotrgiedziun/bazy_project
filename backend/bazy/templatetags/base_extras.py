from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def navactive_contains(request, title):
    for t in title.split():
        if any(t in s for s in request.path.split('/')):
            return "active"
    return ""