from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^ratecontrol/$', views.rate_control, name='rate_control'),
    url(r'^addarticle/$', views.add_article, name='add_article'),
    url(r'^addcomment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
    url(r'^delcomment/(?P<comment_id>[0-9]+)/$', views.del_comment, name='del_comment'),
]
