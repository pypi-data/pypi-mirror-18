from django.conf.urls import url

from .views import callback, auth, endpoint

urlpatterns = [
    url(r'cb$', callback, name='deviantart-cb'),
    url(r'auth$', auth, name='deviantart-auth'),
    url(r'^([\w\-/]*)$', endpoint)
]
