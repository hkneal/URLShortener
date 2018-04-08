from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import CreateView, GetView, GetNickNameView

urlpatterns = [
    url(r'^$', views.index),
    url(r'^Shorten$', views.shortenURL, name = 'shortenURL'),
    url(r'^(?P<nick_name>\w+)$', views.expandURL, name='expandURL'),
    url(r'^Shorten/original$', views.returnExpanded, name='returnExpanded'),
    url(r'^api/post$', CreateView.as_view(), name="create"),
    url(r'^api/get$', GetView.as_view(), name="get"),
    url(r'^api/get/(?P<nick_name>\w+)$', GetNickNameView.as_view(), name="getNickName")
    #url(r'^api/delete/(?P<nick_name>\w+)$', DeleteNickNameView.as_view(), name="DeleteNickName"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
