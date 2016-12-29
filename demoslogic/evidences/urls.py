from django.conf.urls import url

from . import views

app_name = 'evidences'
urlpatterns = [
    url(r'^create$', views.EvidenceCreateView.as_view(), name = 'create'),
    url(r'^(?P<pk>[0-9]+)/$', views.EvidenceDetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[0-9]+)/update_vote$', views.EvidenceUpdateView.as_view(), name = 'update_vote'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.DeleteEvidenceView.as_view(), name = 'delete'),
    # url(r'^(?P<premise_id>[0-9]+)/vote/$', views.vote, name = 'vote'),
]
