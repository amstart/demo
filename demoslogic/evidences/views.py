from dal import autocomplete
from switch import Switch
from itertools import chain

from django.views.generic import TemplateView, FormView, DetailView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from demoslogic.blockobjects import views

from . import forms, models
from demoslogic.premises.models import Premise

# from .forms import EvidenceCreateForm, EvidenceVoteForm, SearchEvidenceForm

class EvidenceDetailView(views.DetailWithVoteView):
    model = models.Evidence
    voteform = forms.EvidenceVoteForm


class EvidenceCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
    success_url = '/'
    model = models.Evidence

    def get_form_class(self):#, form_class=None):
        return forms.EvidenceCreateForm

    def get_form_kwargs(self):
        kwargs = super(EvidenceCreateView, self).get_form_kwargs()
        kwargs['statement'] = self.request.GET.get('statement')
        return kwargs#(premise1 = premise1, premise2 = premise2, conclusion = conclusion)


class DeleteEvidenceView(views.DeleteObjectView):
    model = models.Evidence
    success_url = reverse_lazy('premises:index')

class EvidenceUpdateView(views.UpdateVoteView):
    model = models.Evidence
    voteform = forms.EvidenceVoteForm
