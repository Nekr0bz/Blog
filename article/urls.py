from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^articleaddlike/(?P<article_id>[0-9]+)/$', views.article_add_like, name='article_add_like'),
    url(r'^articleadddislike/(?P<article_id>[0-9]+)/$', views.article_add_dislike, name='article_add_dislike'),
    url(r'^commentaddlike/(?P<comment_id>[0-9]+)/$', views.comment_add_like, name='comment_add_like'),
    url(r'^commentadddislike/(?P<comment_id>[0-9]+)/$', views.comment_add_dislike, name='comment_add_dislike'),
]