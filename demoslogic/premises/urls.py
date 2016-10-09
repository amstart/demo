from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'premises'
urlpatterns = [
    url(r'^$', views.PremisesListView.as_view(), name = 'index'),
    url(r'^unstaged/$', views.UnstagedPremisesListView.as_view(), name = 'unstaged'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeletePremiseView.as_view(), name = 'delete'),
    url(r'^new/$', views.NewPremiseView.as_view(), name = 'new'),
    url(r'^new/(?P<mode>[a-zA-Z]+)$', login_required(views.PremiseCreateView.as_view()), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PremiseDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.PremiseVotesView.as_view(), name = 'results'),
    url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
