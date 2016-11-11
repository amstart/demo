from django.conf.urls import url

from . import views

app_name = 'premises'
urlpatterns = [
    url(r'^$', views.PremisesListView.as_view(), name = 'index'),
    url(r'^autocomplete$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^unstaged/$', views.PremisesListView.as_view(), name = 'unstaged'),
    url(r'^search/$', views.PremiseSearchView.as_view(), name = 'search'),
    url(r'^new/$', views.NewPremiseView.as_view(), name = 'new'),
    url(r'^new/(?P<mode>[a-zA-Z]+)$', views.PremiseCreateView.as_view(), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PremiseDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/update_vote$', views.PremiseUpdateView.as_view(), name = 'update_vote'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeletePremiseView.as_view(), name = 'delete'),
    # url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
