from django.conf.urls import url

from . import views

app_name = 'premises'
urlpatterns = [
    url(r'^$', views.PremisesListView.as_view(), name = 'index'),
    url(r'^autocomplete$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^nouns/autocomplete_create$', views.NounAutocomplete.as_view(create_field='name'),
        name = 'nouns_autocomplete_create'),
    url(r'^predicates/autocomplete_create$', views.PredicateAutocomplete.as_view(create_field='name'),
        name = 'predicates_autocomplete_create'),
    url(r'^complements/autocomplete_create$', views.ComplementAutocomplete.as_view(create_field='name'),
        name = 'complements_autocomplete_create'),
    url(r'^nouns/autocomplete$', views.NounAutocomplete.as_view(),
        name = 'nouns_autocomplete'),
    url(r'^predicates/autocomplete$', views.PredicateAutocomplete.as_view(),
        name = 'predicates_autocomplete'),
    url(r'^complements/autocomplete$', views.ComplementAutocomplete.as_view(),
        name = 'complements_autocomplete'),
    # url(r'^nouns/$', views.PremiseAutocomplete.as_view(), name = 'autocomplete'),
    url(r'^unstaged/$', views.PremisesListView.as_view(), name = 'unstaged'),
    url(r'^search/$', views.PremiseSearchView.as_view(), name = 'search'),
    url(r'^nouns/search/$', views.NounSearchView.as_view(), name = 'search_nouns'),
    url(r'^predicates/search/$', views.PredicateSearchView.as_view(), name = 'search_predicates'),
    url(r'^complements/search/$', views.ComplementSearchView.as_view(), name = 'search_complements'),
    url(r'^create$', views.PremiseCreateView.as_view(), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PremiseDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/update_vote$', views.PremiseUpdateView.as_view(), name = 'update_vote'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeletePremiseView.as_view(), name = 'delete'),
    # url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
