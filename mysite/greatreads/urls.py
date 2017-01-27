from django.conf.urls import url

from . import views

app_name = 'greatreads'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<search_id>[0-9]+)/searchpage/$', views.searchpage, name='searchpage'),
]

#'the hard way'
# urlpatterns = [
#     # ex: /greatreads/
#     url(r'^$', views.index, name='index'),
#     # ex: /greatreads/5/
#     url(r'^(?P<search_id>[0-9]+)/$', views.detail, name='detail'),
#     # ex: /greatreads/5/results/
#     url(r'^(?P<search_id>[0-9]+)/results/$', views.results, name='results'),
#     # ex: /greatreads/5/vote/
#     url(r'^(?P<search_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
