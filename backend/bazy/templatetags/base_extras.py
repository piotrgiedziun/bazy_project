from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    for url in urls.split():
        if url[0] == "_":
            if any(url[1:] in s for s in request.path.split('/')):
                return "active"
        elif request.path in reverse(url):
            return "active"
    return ""

@register.simple_tag
def navactive_contains(request, title):
    for t in title.split():
        if any(t in s for s in request.path.split('/')):
            return "active"
    return ""

@register.filter
def pln(pln):
    dollars = round(float(pln), 2)
    return "%s%s PLN" % (int(pln), ("%0.2f" % pln)[-3:])