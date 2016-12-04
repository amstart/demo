from django.conf.urls import url

from . import views

app_name = 'premises'
urlpatterns = [
    url(r'^$', views.PremisesListView.as_view(), name = 'index'),
    url(r'^autocomplete$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^nouns/autocomplete_create$', views.NounAutocomplete.as_view(create_field='name'),
        name = 'nouns_autocomplete_create'),
    url(r'^verbs/autocomplete_create$', views.VerbAutocomplete.as_view(create_field='name'),
        name = 'verbs_autocomplete_create'),
    url(r'^adjectives/autocomplete_create$', views.AdjectiveAutocomplete.as_view(create_field='name'),
        name = 'adjectives_autocomplete_create'),
    url(r'^nouns/autocomplete$', views.NounAutocomplete.as_view(),
        name = 'nouns_autocomplete'),
    url(r'^verbs/autocomplete$', views.VerbAutocomplete.as_view(),
        name = 'verbs_autocomplete'),
    url(r'^adjectives/autocomplete$', views.AdjectiveAutocomplete.as_view(),
        name = 'adjectives_autocomplete'),
    # url(r'^nouns/$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^unstaged/$', views.PremisesListView.as_view(), name = 'unstaged'),
    url(r'^search/$', views.PremiseSearchView.as_view(), name = 'search'),
    url(r'^nouns/search/$', views.NounSearchView.as_view(), name = 'search_nouns'),
    url(r'^nouns/(?P<pk>[0-9]+)/$', views.NounDetailView.as_view(), name = 'nouns'),
    url(r'^verbs/(?P<pk>[0-9]+)/$', views.VerbDetailView.as_view(), name = 'verbs'),
    url(r'^adjectives/(?P<pk>[0-9]+)/$', views.AdjectiveDetailView.as_view(), name = 'adjectives'),
    url(r'^verbs/search/$', views.VerbSearchView.as_view(), name = 'search_verbs'),
    url(r'^adjectives/search/$', views.AdjectiveSearchView.as_view(), name = 'search_adjectives'),
    url(r'^new/$', views.NewPremiseView.as_view(), name = 'new'),
    url(r'^create$', views.PremiseCreateView.as_view(), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PremiseDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/update_vote$', views.PremiseUpdateView.as_view(), name = 'update_vote'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeletePremiseView.as_view(), name = 'delete'),
    # url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
