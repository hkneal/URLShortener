from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^shortenURL$', views.shortenURL, name = 'shortenURL'),
    url(r'^shortenURL/(?P<nick_name>\w+)$', views.expandURL, name='expandURL')
    #url(r'^shortenURL/original$', views.returnExpanded, name='returnExpanded')
]
