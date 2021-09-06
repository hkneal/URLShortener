from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import CreateView, GetView, GetNickNameView

urlpatterns = [
    path('', views.index),
    path('Shorten/', views.shortenURL, name='shortenURL'),
    # path('Shorten/<nick_name>/', views.expandURL, name='expandURL'),
    re_path(r'^(?P<nick_name>\w+)$', views.expandURL, name='expandURL'),
    path('Shorten/original/', views.returnExpanded, name='returnExpanded'),
    path('api/post/', CreateView.as_view(), name="create"),
    path('api/get/', GetView.as_view(), name="get"),
    path('api/get/<nick_name>', GetNickNameView.as_view(), name="getNickName")
    # re_path(r'^api/get/(?P<nick_name>\w+)$', GetNickNameView.as_view(), name="getNickName")
    #url(r'^api/delete/(?P<nick_name>\w+)$', DeleteNickNameView.as_view(), name="DeleteNickName"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
