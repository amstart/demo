from switch import Switch

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.utils import timezone

from demoslogic.users.models import User
from demoslogic.blockobjects.views import DetailWithVoteView, UpdateVoteView, CreateObjectView, ObjectListView

from .models import Premise, CategorizationVote
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseDetailView(DetailWithVoteView):
    model = Premise
    template_name = 'premises/detail.html'
    voteform = CategorizationVoteForm()

class PremiseUpdateView(UpdateVoteView):
    model = Premise
    template_name = 'blockobjects/update_vote.html'
    voteform = CategorizationVoteForm()

class NewPremiseView(TemplateView):
    template_name = 'premises/new_premise.html'

class PremiseCreateView(CreateObjectView):
    template_name = 'premises/create_premise.html'
    success_url = '/'
    model = Premise

    def get_form_class(self):
        with Switch(self.kwargs['mode']) as case:
            if case('SubjectPredicate'):
                return SubjectPredicateInputForm
            if case('WithComplementedObject'):
                return WithComplementedObjectInputForm
            if case('WithObject'):
                return WithObjectInputForm
            if case('WithComplement'):
                return WithComplementInputForm

    def form_valid(self, form):
        super(PremiseCreateView, self).form_valid(form)
        return HttpResponseRedirect(reverse('premises:detail', args = [self.object.pk]))

class PremisesListView(ObjectListView):
    model = Premise

class DeletePremiseView(DeleteView):
    template_name = 'blockobjects/delete_object.html'
    model = Premise
    success_url = reverse_lazy('premises:index')
