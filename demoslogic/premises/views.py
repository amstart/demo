from switch import Switch

from django.views.generic import TemplateView
from django.core.urlresolvers import reverse, reverse_lazy

from demoslogic.blockobjects import views

from .models import Premise
from .forms import SubjectPredicateInputForm, WithComplementedObjectInputForm, WithObjectInputForm, WithComplementInputForm
from .forms import CategorizationVoteForm

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
