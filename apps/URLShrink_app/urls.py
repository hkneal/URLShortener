from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^Shorten$', views.shortenURL, name = 'shortenURL'),
    url(r'^(?P<nick_name>\w+)$', views.expandURL, name='expandURL'),
    url(r'^Shorten/original$', views.returnExpanded, name='returnExpanded')
]
