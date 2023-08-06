from deviantart.oauth import Deviantart
from django import template
from django.http.request import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def dA(context, endpoint, **params):
    deviantart = Deviantart()
    qd = QueryDict(mutable=True)
    qd.update(params)
    return deviantart.get(endpoint + '?' + qd.urlencode())
