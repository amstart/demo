from django.conf.urls import url

from . import views

app_name = 'arguments'
urlpatterns = [
    url(r'^$', views.ArgumentsListView.as_view(), name = 'index'),
    url(r'^autocomplete$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^unstaged/$', views.ArgumentsListView.as_view(), name = 'unstaged'),
    url(r'^new/$', views.NewArgumentView.as_view(), name = 'new'),
    url(r'^new/create$', views.ArgumentCreateView.as_view(), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArgumentDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/update_vote$', views.ArgumentUpdateView.as_view(), name = 'update_vote'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeleteArgumentView.as_view(), name = 'delete'),
    # url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
