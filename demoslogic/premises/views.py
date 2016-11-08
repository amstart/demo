from dal import autocomplete
from switch import Switch

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q

from demoslogic.blockobjects import views

from .models import Premise
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

class PremiseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated():
        #     return Premise.objects.none()
        qs = Premise.objects.all()
        premise1 = self.forwarded.get('premise1', None)
        premise2 = self.forwarded.get('premise2', None)
        conclusion = self.forwarded.get('conclusion', None)
        if premise1:
            qs = qs.exclude(id=premise1)
        if premise2:
            qs = qs.exclude(id=premise2)
        if conclusion:
            qs = qs.exclude(id=conclusion)
        if self.q:
            # premise2 = self.forwarded.get('premise2', None)
            # conclusion = self.forwarded.get('conclusion', None)
            # qs = Premise.objects.raw("SELECT * FROM Premise WHERE %s == CONCAT(premise1, premise2)", [self.q])
            qs = qs.filter(Q(subject__contains=self.q)
                           | Q(predicate__contains=self.q)
                           | Q(object__contains=self.q)
                           | Q(complement__contains=self.q))
        return qs

class PremiseDetailView(views.DetailWithVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

    def get_context_data(self, **kwargs):
        context = super(PremiseDetailView, self).get_context_data(**kwargs)
        context['as_premise_set'] = self.object.premise1.filter()
        context['as_conclusion_set'] = self.object.conclusion.filter()
        return context

class PremiseUpdateView(views.UpdateVoteView):
    model = Premise
    voteform = CategorizationVoteForm()

class NewPremiseView(TemplateView):
    template_name = 'premises/new_premise.html'

class PremiseCreateView(views.CreateObjectView):
    template_name = 'blockobjects/create_object.html'
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

class PremisesListView(views.ObjectListView):
    model = Premise

class DeletePremiseView(views.DeleteObjectView):
    model = Premise
    success_url = reverse_lazy('premises:index')
