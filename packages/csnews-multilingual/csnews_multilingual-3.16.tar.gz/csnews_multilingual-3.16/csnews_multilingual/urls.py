from django.conf.urls import patterns, url, include
from csnews_multilingual.feeds import LatestNews
from django.utils.translation import ugettext_lazy as _
# feed_dict = {'rss': LatestNews}


urlpatterns = patterns(
    'csnews_multilingual.views',
    url(r'^$', 'index', name='csnews_index'),
    url(_(r'^tag/(?P<tag_slug>[\-\d\w]+)/$'), 'tag_index', name='csnews_tag'),
    url(_(r'^feed/$'), LatestNews(), name='csnews_feed'),
    url(_(r'^archive/$'), 'archive', name='csnews_archive'),
    url(_(r'^(?P<article_slug>[\-\d\w]+)/$'), 'article_index', name='csnews_article'),
)
